# esrally对elasticsearch进行压力测试



最近需要对项目中es集群进行压力测试，所以选择esrally。但是由于它默认提供的测试数据均是英文，不贴合实际情况，所以需要自定义测试数据与测试用例来进行测试。


### 创建自定义的测试集
```
esrally create-track --track=cme --target-hosts=192.168.9.239:9200 --client-options="basic_auth_user:'elastic',basic_auth_password:'EC05E3BB626EBB7FB06052614C453ACF'" --indices="zn_v2" --output-path=~/tracks
```

### 进行压力测试,并指定测试数据为自定义测试集
```
 esrally race --pipeline=benchmark-only --target-hosts=192.168.9.239:9200,192.168.9.238:9200,192.168.9.240:9200  --track-path=/root/tracks/zn/  --client-options="basic_auth_user:'elastic',basic_auth_password:'EC05E3BB626EBB7FB06052614C453ACF'"
```

### 配置自定义的测试用例
> track.json
```
[root@localhost zn]# cat track.json
{% import "rally.helpers" as rally with context %}
{
  "version": 2,
  "description": "Tracker-generated track for zn",
  "indices": [
    {
      "name": "zn_v2",
      "body": "zn_v2.json"
    }
  ],
  "corpora": [
    {
      "name": "zn_v2",
      "documents": [
        {
          "target-index": "zn_v2",
          "source-file": "zn_v2-documents.json.bz2",
          "document-count": 1411125,
          "compressed-bytes": 740757851,
          "uncompressed-bytes": 4081869683
        }
      ]
    }
  ],
  "challenges": [
    {% include "challenges/index-and-query.json" %}
  ]
}
```

> index-and-query.json
```
{
  "name": "index-and-query",
  "default": true,
  "schedule": [
    {
      "operation": {
        "operation-type": "delete-index"
      }
    },
    {
      "operation": {
        "operation-type": "create-index"
      }
    },
    {
      "operation": {
        "operation-type": "bulk",
        "bulk-size": 1000
      },
      "warmup-time-period": 120,
      "clients": 100
    },
    {
      "operation": {
        "operation-type": "force-merge"
      }
    },
    {
      "operation": {
        "name": "query-match-all",
        "operation-type": "search",
        "body": {
          "query": {
            "match_all": {}
          }
        }
      },
      "clients": 8,
      "warmup-iterations": 1,
      "iterations": 100,
      "target-throughput": 100
    },
    {
      "operation": {
        "name": "query-match-1",
        "operation-type": "search",
        "body": {
          "query": {
            "term": {
              "sen6": {
                "value": "夫人"
              }
            }
          }
        }
      },
      "clients": 8,
      "warmup-iterations": 1,
      "iterations": 100,
      "target-throughput": 100
    },
    {
      "operation": {
        "name": "query-match-6",
        "operation-type": "search",
        "body": {
          "from": 0,
          "size": 20,
          "query": {
            "bool": {
              "must": [
                {
                  "multi_match": {
                    "query": "测试",
                    "fields": [
                      "*^1.0"
                    ],
                    "type": "best_fields",
                    "operator": "OR",
                    "slop": 0,
                    "prefix_length": 0,
                    "max_expansions": 50,
                    "minimum_should_match": "75%",
                    "zero_terms_query": "NONE",
                    "auto_generate_synonyms_phrase_query": true,
                    "fuzzy_transpositions": true,
                    "boost": 1
                  }
                }
              ],
              "adjust_pure_negative": true,
              "boost": 1
            }
          },
          "highlight": {
            "pre_tags": [
              "<font color='red'>"
            ],
            "post_tags": [
              "</font>"
            ],
            "fields": {
              "*": {}
            }
          }
        }
      },
      "clients": 8,
      "warmup-iterations": 1,
      "iterations": 100,
      "target-throughput": 100
    }
  ]
}
```
> 查询的测试用例，可以先用kibana进行查询测试通过后，直接将查询json复制到`body`中，
> clients表示客户端并发数
> warmup-iterations表示每个客户端的迭代数量
> iterations表示每个迭代数中循环测试
> target-throughput表示目标吞吐量大小

注：
1、使用自定义测试数据集，最好使用一个索引的文件数据即可，否则自定义查询用例时会报错
2、设置其并发数与迭代数，需要谨慎，否则导致测试端挂死（需要提高测试端的配置）、服务端挂死（提供服务端的配置）、测试时间超长（减少并发数或者迭代数）。