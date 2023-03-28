from rest_framework.pagination import PageNumberPagination


class PageLimitPagination(PageNumberPagination):
    """Стандартный пагинатор"""
    page_size_query_param = 'limit'


class SubPagination(PageNumberPagination):
    page_size_query_param = 'recipes_limit'
    max_page_size = 3

    def get_page_size(self, request):
        if self.page_size_query_param:
            try:
                return int(request.query_params[self.page_size_query_param])
            except (KeyError, ValueError):
                pass
        return self.page_size
