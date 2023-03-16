from rest_framework.pagination import PageNumberPagination


class PaginationNone(PageNumberPagination):
    """Класс для сериализаторов без пагинации"""
    page_size = None
