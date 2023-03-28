from rest_framework.pagination import PageNumberPagination


class PageLimitPagination(PageNumberPagination):
    """Стандартный пагинатор"""
    page_size_query_param = 'limit'
