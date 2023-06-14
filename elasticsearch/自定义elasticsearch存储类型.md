# 全文检索中 timestamp类型的数据插入elasticsearch



###在进行全文检索中需要将MySQL、oracle等数据库中数据进行采集，批量插入到ES中。但是在进行插入timestamp类型的数据时，插入失败，错误信息如下：
```
java.lang.IllegalArgumentException: cannot write xcontent for unknown value of type class java.sql.Timestamp
```

## 数据批量插入方法
```
    public static void insertOrUpdate(String indexName, String pkName, RestHighLevelClient client, List<Map<String, Object>> elements) {
        BulkRequest bulkRequest = new BulkRequest();
        bulkRequest.timeout("10s");
        for (Map<String, Object> element : elements) {
            IndexRequest createRequest = new IndexRequest(indexName);
            createRequest.id(element.get(pkName).toString());
            createRequest.source(element);
            UpdateRequest updateRequest = new UpdateRequest(indexName, element.get(pkName).toString());
            // 如果文档尚不存在，则可以使用以下方法定义一些将作为新文档插入的内容
            updateRequest.doc(element).upsert(createRequest);
            // 添加文档
            bulkRequest.add(createRequest);
            // 更新文档
            bulkRequest.add(updateRequest);
        }
        client.bulk(bulkRequest, RequestOptions.DEFAULT);
    }
```

#### 追踪createRequest.source的执行流程,可以找到XContentBuilder类中unknownValue方法

```
    private void unknownValue(Object value, boolean ensureNoSelfReferences) throws IOException {
        if (value == null) {
            nullValue();
            return;
        }
        Writer writer = WRITERS.get(value.getClass());
        if (writer != null) {
            writer.write(this, value);
        } else if (value instanceof Path) {
            //Path implements Iterable<Path> and causes endless recursion and a StackOverFlow if treated as an Iterable here
            value((Path) value);
        } else if (value instanceof Map) {
            @SuppressWarnings("unchecked")
            final Map<String, ?> valueMap = (Map<String, ?>) value;
            map(valueMap, ensureNoSelfReferences, true);
        } else if (value instanceof Iterable) {
            value((Iterable<?>) value, ensureNoSelfReferences);
        } else if (value instanceof Object[]) {
            values((Object[]) value, ensureNoSelfReferences);
        } else if (value instanceof ToXContent) {
            value((ToXContent) value);
        } else if (value instanceof Enum<?>) {
            // Write out the Enum toString
            value(Objects.toString(value));
        } else {
            throw new IllegalArgumentException("cannot write xcontent for unknown value of type " + value.getClass());
        }
    }
```

#### 发现直接走的`else`，抛出异常，也就意味着没有对Timestamp类型进行判断。
#### 然后我们查看`WRITERS`变量中,包含哪些数据类型，以及是否提供扩展接口。
```
static {
        Map<Class<?>, Writer> writers = new HashMap<>();
        writers.put(Boolean.class, (b, v) -> b.value((Boolean) v));
        // ....


        Map<Class<?>, HumanReadableTransformer> humanReadableTransformer = new HashMap<>();
        Map<Class<?>, Function<Object, Object>> dateTransformers = new HashMap<>();

        // treat strings as already converted
        dateTransformers.put(String.class, Function.identity());

        // Load pluggable extensions
        for (XContentBuilderExtension service : ServiceLoader.load(XContentBuilderExtension.class)) {
            Map<Class<?>, Writer> addlWriters = service.getXContentWriters();
            Map<Class<?>, HumanReadableTransformer> addlTransformers = service.getXContentHumanReadableTransformers();
            Map<Class<?>, Function<Object, Object>> addlDateTransformers = service.getDateTransformers();

            addlWriters.forEach((key, value) -> Objects.requireNonNull(value,
                "invalid null xcontent writer for class " + key));
            addlTransformers.forEach((key, value) -> Objects.requireNonNull(value,
                "invalid null xcontent transformer for human readable class " + key));
            dateTransformers.forEach((key, value) -> Objects.requireNonNull(value,
                "invalid null xcontent date transformer for class " + key));

            writers.putAll(addlWriters);
            humanReadableTransformer.putAll(addlTransformers);
            dateTransformers.putAll(addlDateTransformers);
        }

        WRITERS = Collections.unmodifiableMap(writers);
        HUMAN_READABLE_TRANSFORMERS = Collections.unmodifiableMap(humanReadableTransformer);
        DATE_TRANSFORMERS = Collections.unmodifiableMap(dateTransformers);
    }
```
#### 发现`WRITERS`先进行类型的添加，然后通过`ServiceLoader.load`进行动态的扩展数据类型。
#### 它这是SPI机制。SPI（Service Provider Interface），是JDK内置的一种服务提供发现机制，可以用来启用框架扩展和替换组件。
####　接下来擦好看XContentBuilderExtension接口的实现类XContentElasticsearchExtension，发现它对部分时间类型进行配置，但是没有Timestamp类型。
```
public class XContentElasticsearchExtension implements XContentBuilderExtension {

    public static final DateTimeFormatter DEFAULT_DATE_PRINTER = ISODateTimeFormat.dateTime().withZone(DateTimeZone.UTC);
    public static final DateFormatter DEFAULT_FORMATTER = DateFormatter.forPattern("strict_date_optional_time_nanos");
    public static final DateFormatter LOCAL_TIME_FORMATTER = DateFormatter.forPattern("HH:mm:ss.SSS");
    public static final DateFormatter OFFSET_TIME_FORMATTER = DateFormatter.forPattern("HH:mm:ss.SSSZZZZZ");

    @Override
    public Map<Class<?>, XContentBuilder.Writer> getXContentWriters() {
        Map<Class<?>, XContentBuilder.Writer> writers = new HashMap<>();

        // Fully-qualified here to reduce ambiguity around our (ES') Version class
        writers.put(DateTimeZone.class, (b, v) -> b.value(Objects.toString(v)));
        writers.put(CachedDateTimeZone.class, (b, v) -> b.value(Objects.toString(v)));
        writers.put(FixedDateTimeZone.class, (b, v) -> b.value(Objects.toString(v)));
        writers.put(MutableDateTime.class, XContentBuilder::timeValue);
        writers.put(DateTime.class, XContentBuilder::timeValue);
        // ...
        return writers;
    }

    @Override
    public Map<Class<?>, XContentBuilder.HumanReadableTransformer> getXContentHumanReadableTransformers() {
        Map<Class<?>, XContentBuilder.HumanReadableTransformer> transformers = new HashMap<>();
        transformers.put(TimeValue.class, v -> ((TimeValue) v).millis());
        transformers.put(ByteSizeValue.class, v -> ((ByteSizeValue) v).getBytes());
        return transformers;
    }

    @Override
    public Map<Class<?>, Function<Object, Object>> getDateTransformers() {
        Map<Class<?>, Function<Object, Object>> transformers = new HashMap<>();
        transformers.put(Date.class, d -> DEFAULT_DATE_PRINTER.print(((Date) d).getTime()));
        transformers.put(DateTime.class, d -> DEFAULT_DATE_PRINTER.print((DateTime) d));
        transformers.put(MutableDateTime.class, d -> DEFAULT_DATE_PRINTER.print((MutableDateTime) d));
        transformers.put(ReadableInstant.class, d -> DEFAULT_DATE_PRINTER.print((ReadableInstant) d));
        // ...
        return transformers;
    }
}

```
####　接下来找到｀org.elasticsearch:elasticsearch｀包，｀META-INF｀文件夹下的`services`有一个`org.elasticsearch.common.xcontent.XContentBuilderExtension`文件，而文件中则有一个`org.elasticsearch.common.xcontent.XContentElasticsearchExtension`类路径

## 扩展Timestamp类型
#### 模拟XContentElasticsearchExtension类，创建CustomXContentElasticsearchExtension类，进行扩展Timestamp类型
```
import org.elasticsearch.common.xcontent.XContentBuilder;
import org.elasticsearch.common.xcontent.XContentBuilderExtension;
import org.joda.time.DateTimeZone;
import org.joda.time.format.DateTimeFormatter;
import org.joda.time.format.ISODateTimeFormat;

import java.sql.Timestamp;
import java.util.HashMap;
import java.util.Map;
import java.util.function.Function;

public class CustomXContentElasticsearchExtension implements XContentBuilderExtension {

    public static final DateTimeFormatter DEFAULT_DATE_PRINTER = ISODateTimeFormat.dateTime().withZone(DateTimeZone.UTC);

    @Override
    public Map<Class<?>, XContentBuilder.Writer> getXContentWriters() {
        Map<Class<?>, XContentBuilder.Writer> writers = new HashMap<>();

        // Fully-qualified here to reduce ambiguity around our (ES') Version class
        writers.put(Timestamp.class, XContentBuilder::timeValue);
        writers.put(java.sql.Date.class, XContentBuilder::timeValue);

        return writers;
    }

    @Override
    public Map<Class<?>, XContentBuilder.HumanReadableTransformer> getXContentHumanReadableTransformers() {
        return new HashMap<>();
    }

    @Override
    public Map<Class<?>, Function<Object, Object>> getDateTransformers() {
        Map<Class<?>, Function<Object, Object>> transformers = new HashMap<>();
        transformers.put(Timestamp.class, d -> DEFAULT_DATE_PRINTER.print(((Timestamp) d).getTime()));
        transformers.put(java.sql.Date.class, d -> DEFAULT_DATE_PRINTER.print(((java.sql.Date) d).getTime()));
        return transformers;
    }
}
```
#### 在自己的项目的`resources`下，创建一个`META-INF`文件夹，在文件夹中添加一个`org.elasticsearch.common.xcontent.XContentBuilderExtension`,在文件中添加原本类`XContentElasticsearchExtension`的全路径与自定类`CustomXContentElasticsearchExtension`的全路径