from rest_framework.pagination import PageNumberPagination


class PageLimitPagination(PageNumberPagination):
    page_size = 'limit'

class SubPagination(PageNumberPagination):
    page_size_query_param = 3
