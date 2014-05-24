from rest_framework_extensions.key_constructor.constructors import DefaultKeyConstructor
from rest_framework_extensions.key_constructor.bits import (
    KeyBitBase,
    RetrieveSqlQueryKeyBit,
    ListSqlQueryKeyBit,
    PaginationKeyBit,
    UserKeyBit,
    QueryParamsKeyBit
)


class DefaultPaginatedListKeyConstructor(DefaultKeyConstructor):
    page = QueryParamsKeyBit(
        ['page',]
    )
