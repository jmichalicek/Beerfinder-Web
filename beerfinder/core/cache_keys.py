from rest_framework_extensions.key_constructor.constructors import DefaultKeyConstructor
from rest_framework_extensions.key_constructor.bits import (
    ArgsKeyBit,
    KwargsKeyBit,
    KeyBitBase,
    RetrieveSqlQueryKeyBit,
    ListSqlQueryKeyBit,
    PaginationKeyBit,
    UserKeyBit,
    QueryParamsKeyBit
)


class QueryParamsKeyConstructor(DefaultKeyConstructor):
    query_params = QueryParamsKeyBit('*')


class DefaultPaginatedListKeyConstructor(DefaultKeyConstructor):
    page = QueryParamsKeyBit(
        ['page',]
    )
