# elasticsearch的查询数大于10000查询失败



### 错误信息
```
Caused by: ElasticsearchException[Elasticsearch exception [type=illegal_argument_exception, reason=Result window is too large, from + size must be less than or equal to: [10000] but was [11000]. See the scroll api for a more efficient way to request large data sets. This limit can be set by changing the [index.max_result_window] index level setting.]]; nested: ElasticsearchException[Elasticsearch exception [type=illegal_argument_exception, reason=Result window is too large, from + size must be less than or equal to: [10000] but was [11000]. See the scroll api for a more efficient way to request large data sets. This limit can be set by changing the [index.max_result_window] index level setting.]];
	at org.elasticsearch.ElasticsearchException.innerFromXContent(ElasticsearchException.java:491)
	at org.elasticsearch.ElasticsearchException.fromXContent(ElasticsearchException.java:402)
	at org.elasticsearch.ElasticsearchException.innerFromXContent(ElasticsearchException.java:432)
	at org.elasticsearch.ElasticsearchException.failureFromXContent(ElasticsearchException.java:598)
	at org.elasticsearch.rest.BytesRestResponse.errorFromXContent(BytesRestResponse.java:170)
	... 122 more
```

### 错误原因
elasticsearch官方提及:不能使用from和size翻阅超过 10,000 个点击。此限制是由`index.max_result_window`索引设置设置的保护措施。

## 处理方法：
### 方法1.增加max_result_window的大小
```
PUT tweets_v1/_settings
{
    "index": {
        "max_result_window": 1000000
    }
}
```
注：手动增加`max_result_window`大小，会导致内存与CPU占用过高，并且不好保证手动设置的大小，在一定时间后会不会任然够用，故而不推荐使用。

### 方法2.使用Scroll API（滚动查询）
```
    @Resource
    private ElasticsearchRestTemplate template;

    // 第一次获取数据
    public ScrollPageResult<TweetsEntity> scrollStart(Integer pageSize) {
        NativeSearchQuery nativeSearchQuery = new NativeSearchQueryBuilder()
                .withSort(new FieldSortBuilder("createTime"))
                .build();
        // 设置每页数据量
        nativeSearchQuery.setMaxResults(pageSize);
        // 设置滚动id的存在时间
        long scrollTimeInMillis = 600 * 1000;
        // 第一次查询
        SearchScrollHits<TweetsEntity> searchScrollHits = template.searchScrollStart(scrollTimeInMillis, nativeSearchQuery, TweetsEntity.class, IndexCoordinates.of("tweets_v1"));

        // 获取下一次的滚动id，时间有限
        String scrollId = searchScrollHits.getScrollId();

        // 获取数据
        List<TweetsEntity> results = new ArrayList<>();
        searchScrollHits.getSearchHits().iterator().forEachRemaining(item -> results.add(item.getContent()));

        // 数据返回
        return ScrollPageResult.of(scrollId, results);
    }

    // 获取下一页数据
    public ScrollPageResult<TweetsEntity> scrollNext(String scrollId) {
        long scrollTimeInMillis = 60 * 1000;
        SearchScrollHits<TweetsEntity> searchScrollHits = template.searchScrollContinue(scrollId, scrollTimeInMillis, TweetsEntity.class, IndexCoordinates.of("tweets_v1"));

        // 获取下一次的滚动id，时间有限
        String scrollId2 = searchScrollHits.getScrollId();

        // 获取数据
        List<TweetsEntity> results = new ArrayList<>();
        searchScrollHits.getSearchHits().iterator().forEachRemaining(item -> results.add(item.getContent()));

        if (searchScrollHits.hasSearchHits()) {
            // 数据返回
            return ScrollPageResult.of(scrollId2, results);
        } else {
            // 清除 scroll
            template.searchScrollClear(Collections.singletonList(scrollId2));
            // 数据返回
            return ScrollPageResult.of(null, results);
        }
    }
```
注：elasticsearch官方也是不推荐使用Scroll API的。
一是滚动搜索的结果反映了初始搜索请求时的索引状态，随后的索引或文档更改只会影响以后的搜索和滚动请求；
二是Scroll API需要Scroll ID。要获取Scroll ID，则需要设置请求保留搜索上下文多长时间，只有在时间中生成的Scroll ID才有效。

### 方法3.使用search_after参数
```
    @Resource
    private ElasticsearchRestTemplate template;
    // 第一次获取
    public SearchAfterPageResult<TweetsEntity> searchAfterStart(Integer pageSize) {
        NativeSearchQuery searchQuery = new NativeSearchQueryBuilder()
                .withQuery(QueryBuilders.matchAllQuery())
                .withPageable(Pageable.ofSize(pageSize))
                .withSort(Sort.by("createTime")).build();
        SearchHits<TweetsEntity> search = template.search(searchQuery, TweetsEntity.class, IndexCoordinates.of("tweets_v1"));
        List<SearchHit<TweetsEntity>> list = search.getSearchHits();

        // 获取数据
        List<TweetsEntity> results = new ArrayList<>();
        search.getSearchHits().iterator().forEachRemaining(item -> results.add(item.getContent()));

        // 数据返回
        return SearchAfterPageResult.of(list.get(list.size() - 1).getSortValues(), results);
    }

    // 获取下一页数据
    public SearchAfterPageResult<TweetsEntity> searchAfterNext(List<Object> searchAfter, Integer pageSize) {
        NativeSearchQuery searchQuery = new NativeSearchQueryBuilder()
                .withQuery(QueryBuilders.matchAllQuery())
                .withPageable(Pageable.ofSize(pageSize))
                .withSearchAfter(searchAfter)
                .withSort(Sort.by("createTime")).build();
        SearchHits<TweetsEntity> search = null;
        try {
            search = template.search(searchQuery, TweetsEntity.class, IndexCoordinates.of("tweets_v1"));
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
        List<SearchHit<TweetsEntity>> list = search.getSearchHits();

        // 获取数据
        List<TweetsEntity> results = new ArrayList<>();
        search.getSearchHits().iterator().forEachRemaining(item -> results.add(item.getContent()));

        // 数据返回
        if (pageSize.equals(results.size())) {
            return SearchAfterPageResult.of(list.get(list.size() - 1).getSortValues(), results);
        } else {
            return SearchAfterPageResult.of(null, results);
        }
    }
```
注： Elasticsearch 使用 Lucene 的内部文档 ID 作为决胜局。这些内部文档 ID 在相同数据的副本中可能完全不同。当分页搜索命中时，您可能偶尔会看到具有相同排序值的文档的排序不一致。
更多详细资料：https://www.elastic.co/guide/en/elasticsearch/reference/7.17/paginate-search-results.html#search-after

> 我使用的elasticsearch高版本，在高版本中官方已经不推荐使用RestHighLevelClient，而是使用ElasticsearchRestTemplate。