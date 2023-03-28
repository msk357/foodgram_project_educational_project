from rest_framework.pagination import PageNumberPagination


class PageLimitPagination(PageNumberPagination):
    """Стандартный пагинатор"""
    page_size_query_param = 'limit'


class SubPagination(PageNumberPagination):
    """Стандартный пагинатор"""
    page_size = 3
