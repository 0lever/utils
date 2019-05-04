# -*- coding: utf-8 -*-

from redis_helper import redising
import elasticsearch


class MyElasticsearch(elasticsearch.Elasticsearch):
    redis_db = None

    def __init__(self, *args, **kwargs):
        self.redis_db = kwargs.pop("redis_db")
        elasticsearch.Elasticsearch.__init__(self, *args, **kwargs)

    @elasticsearch.client.utils.query_params('_source', '_source_exclude', '_source_include',
                                             'allow_no_indices', 'allow_partial_search_results', 'analyze_wildcard',
                                             'analyzer', 'batched_reduce_size', 'default_operator', 'df',
                                             'docvalue_fields', 'expand_wildcards', 'explain', 'from_',
                                             'ignore_unavailable', 'lenient', 'max_concurrent_shard_requests',
                                             'pre_filter_shard_size', 'preference', 'q', 'request_cache', 'routing',
                                             'scroll', 'search_type', 'size', 'sort', 'stats', 'stored_fields',
                                             'suggest_field', 'suggest_mode', 'suggest_size', 'suggest_text',
                                             'terminate_after', 'timeout', 'track_scores', 'track_total_hits',
                                             'typed_keys', 'version')
    def search(self, *args, **kwargs):
        redis_db = self.redis_db
        redis_key_prefix_default = kwargs.pop("redis_key_prefix") if kwargs.has_key(
            "redis_key_prefix") else "_lever_utils"
        redis_key_time_default = kwargs.pop("redis_key_time") if kwargs.has_key(
            "redis_key_time") else 0

        kwargs["request_timeout"] = 300
        kwargs["timeout"] = '600s'

        @redising(db=redis_db, time=redis_key_time_default, redis_key_prefix=redis_key_prefix_default)
        def query(*query_args, **query_kwargs):
            result = elasticsearch.Elasticsearch.search(self, *query_args, **query_kwargs)
            return result

        if self.redis_db is None:
            query_result, query_result_redis_key = elasticsearch.Elasticsearch.search(self, *args, **kwargs), None
        else:
            query_result, query_result_redis_key = query(*args, **kwargs)
        return query_result