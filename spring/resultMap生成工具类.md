# resultMap 生成工具类



## resultMap 生成工具类
```
import java.lang.reflect.Field;
import java.lang.reflect.ParameterizedType;
import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class ResultMapGenerator {

    /**
     * //匹配大写字母的正则
     */
    private static Pattern humpPattern = Pattern.compile("[A-Z]");

    private static List<String> FIELD_TYPE = new ArrayList<>();

    static {
        FIELD_TYPE.add("String");
        FIELD_TYPE.add("Integer");
        FIELD_TYPE.add("String");
        FIELD_TYPE.add("Date");
        FIELD_TYPE.add("Double");
        FIELD_TYPE.add("int");
        FIELD_TYPE.add("double");
        FIELD_TYPE.add("Float");
        FIELD_TYPE.add("Instant");
        FIELD_TYPE.add("Boolean");
        FIELD_TYPE.add("boolean");
    }

    /**
     * 生成ResultMap
     *
     * @param clazz 实体类的Class
     * @return String
     */
    public static String generate(Class<?> clazz) {
        String pkgName = clazz.getName();
        String clazzName = clazz.getSimpleName();
        String resultMapId = Character.toLowerCase(clazzName.charAt(0)) + clazzName.substring(1) + "Map";

        StringBuilder resultMap = new StringBuilder();
        resultMap.append("<resultMap id=\"");
        resultMap.append(resultMapId);
        resultMap.append("\" type=\"");
        resultMap.append(pkgName);
        resultMap.append("\">\n");
        result(clazz, resultMap, 1);
        resultMap.append("</resultMap>");
        return resultMap.toString();
    }


    public static void result(Class<?> clazz, StringBuilder resultMap, int level) {
        Field[] fields = clazz.getDeclaredFields();

        // 基础类型
        for (Field curField : fields) {
            // 设置字段可访问（必须，否则报错）
            curField.setAccessible(true);
            String property = curField.getName();
            Class<?> curFieldType = curField.getType();

            if ("serialVersionUID".equals(property)) {
                continue;//忽略掉这个属性
            }
            String curFieldTypeSimpleName = curFieldType.getSimpleName();
            if (FIELD_TYPE.contains(curFieldTypeSimpleName)) {
                for (int i = 0; i < level; i++) {
                    resultMap.append("\t");
                }
                resultMap.append("<result column=\"");
                resultMap.append(property2Column(property));
                resultMap.append("\" property=\"");
                resultMap.append(property);
                resultMap.append("\" />\n");
            }
        }

        // 自定义对象
        for (Field curField : fields) {
            // 设置字段可访问（必须，否则报错）
            curField.setAccessible(true);
            String property = curField.getName();
            Class<?> curFieldType = curField.getType();
            String curFieldTypeSimpleName = curFieldType.getSimpleName();
            if (!FIELD_TYPE.contains(curFieldTypeSimpleName) && !curFieldType.equals(List.class) && !curFieldType.equals(Collection.class)) {
                try {
                    // 得到泛型里的class类型对象

                    String className = curFieldType.getName();
                    if (className.equals(clazz.getName())) {
                        continue;
                    }
                    for (int i = 0; i < level; i++) {
                        resultMap.append("\t");
                    }
                    resultMap.append("<association property=\"");
                    resultMap.append(property);
                    resultMap.append("\" javaType=\"");
                    resultMap.append(className);
                    resultMap.append("\" >\n");

                    result(curFieldType, resultMap, level + 1);

                    for (int i = 0; i < level; i++) {
                        resultMap.append("\t");
                    }
                    resultMap.append("</association>\n");
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }

        }

        // list
        for (Field curField : fields) {
            // 设置字段可访问（必须，否则报错）
            curField.setAccessible(true);
            String property = curField.getName();
            Class<?> curFieldType = curField.getType();

            if (curFieldType.equals(List.class)) {
                Type genericType = curField.getGenericType();
                if (null == genericType) {
                    continue;
                }
                if (genericType instanceof ParameterizedType) {
                    try {
                        ParameterizedType pt = (ParameterizedType) genericType;
                        // 得到泛型里的class类型对象
                        Class<?> actualTypeArgument = (Class<?>) pt.getActualTypeArguments()[0];
                        Object actualType = actualTypeArgument.newInstance();

                        String className = actualTypeArgument.getName();
                        if (className.equals(clazz.getName())) {
                            continue;
                        }
                        for (int i = 0; i < level; i++) {
                            resultMap.append("\t");
                        }
                        resultMap.append("<collection property=\"");
                        resultMap.append(property);
                        resultMap.append("\" ofType=\"");
                        resultMap.append(className);
                        //....actualType字段处理
                        if (FIELD_TYPE.contains(actualTypeArgument.getSimpleName())) {

                            resultMap.append("\" column=\"");
                            resultMap.append(property2Column(property));
                            resultMap.append("\" >\n");
                            // 基本类型
                            for (int i = 0; i < level + 1; i++) {
                                resultMap.append("\t");
                            }
                            resultMap.append("<result column=\"");
                            resultMap.append(property2Column(property));
                            resultMap.append("\" />\n");

                        } else {
                            resultMap.append("\" >\n");
                            // 对象

                            result(Class.forName(actualTypeArgument.getName()), resultMap, level + 1);
                        }
                        for (int i = 0; i < level; i++) {
                            resultMap.append("\t");
                        }
                        resultMap.append("</collection>\n");
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }
        }

    }

    /**
     * 驼峰转下划线命名
     *
     * @param property
     * @return
     */
    private static String property2Column(String property) {
        Matcher matcher = humpPattern.matcher(property);
        StringBuffer sb = new StringBuffer();
        while (matcher.find()) {
            matcher.appendReplacement(sb, "_" + matcher.group(0).toLowerCase());
        }
        matcher.appendTail(sb);
        return sb.toString();
    }

}
```