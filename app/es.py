import datetime
from pprint import pprint
from elasticsearch import Elasticsearch

from dateutil.parser import parse

from app import config

import app.config as config


es_config = config.ES_Settings()

es = Elasticsearch(
    hosts=[
        es_config.host,
    ],
    port=443,
    http_auth=(es_config.appuser, es_config.password),
    scheme="https",
)

# str type convert to datetime type
def parsing_date(splited_index: str):
    try:
        dt = parse(splited_index)
        return dt.date()
    except:
        return None


# get user event data
def get_user_data(uid: str, stdatetime: datetime, eddatetime: datetime):

    print(f"stdatetime: {stdatetime}, eddatetime: {eddatetime}")
    stdate = stdatetime.date()
    eddate = eddatetime.date()
    indexes = es.indices.get("*").keys()

    new_indexes = []
    for index in indexes:
        index_date = index.split("-")[-1:][0]
        dt = parsing_date(index_date)

        if dt and (dt >= stdate) and (dt <= eddate):
            new_indexes.append(index)

    # 전체 인덱스 검색 빈리스트 이용
    new_indexes = []
    print(f"searching index list: {new_indexes}")
    result = es.search(
        index=new_indexes,
        body={
            "size": 1000,
            "query": {
                "bool": {
                    "must": [{"match": {"uid": uid}}],
                    "filter": [
                        {
                            "range": {
                                "udate": {
                                    "lte": eddatetime,
                                    "gte": stdatetime,
                                }
                            }
                        },
                    ],
                }
            },
        }
    )

    docs_count = result["hits"]["total"]["value"]
    print(f"docs_count: {docs_count}")
    docs = result["hits"]["hits"]
    new_data = []
    searched_index = []
    for i, doc in enumerate(docs):
        data = doc["_source"]
        data["no"] = i + 1
        new_data.append(data)
        index = doc["_index"]
        if index not in searched_index:
            searched_index.append(index)

    # pprint(result)
    print(f"searched index: {searched_index}")
    print_count = 1000
    return new_data, docs_count, searched_index,print_count


# get_recent_data
def get_recent_data( stdatetime: datetime, eddatetime: datetime):
    print(f"stdatetime: {stdatetime}, eddatetime: {eddatetime}")
    result = es.search(
        body={
            "size": 100,
            "query": {
                "bool": {
                    "filter": [
                        {
                            "range": {
                                "udate": {
                                    "lte": eddatetime
                                }
                            }
                        },
                    ]
                }
            },
            "sort":[
                {"udate":{"order":"desc"}}
            ]
        },
    )
    docs_count = result["hits"]["total"]["value"]
    print(f"docs_count: {docs_count}")
    docs = result["hits"]["hits"]
    new_data = []
    searched_index = []
    for i, doc in enumerate(docs):
        data = doc["_source"]
        data["no"] = i + 1
        new_data.append(data)
        index = doc["_index"]
        if index not in searched_index:
            searched_index.append(index)
    print_count = 100
    return new_data, docs_count, searched_index, print_count

# all indexes list
def get_indexes():
    indexes = es.indices.get("*").keys()
    return list(indexes)


"""
https://elasticsearch-py.readthedocs.io/en/master/#tls-ssl-and-authentication
"""
