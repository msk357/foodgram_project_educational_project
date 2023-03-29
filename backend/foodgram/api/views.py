from api.permissions import AuthorStaffOrReadOnly, AdminOrReadOnly
from api.mixins import CreateDelViewMixin
from api.paginations import PageLimitPagination
from api.serializers import (
    TagSerializer,
    IngredientSerializer,
    UserSubscribeSerializer,
    RecipeSerializer,
    CropRecipeSerializer,
)
from recipes.models import Tag, Ingredient, Recipe, Favorit, Cart
from users.models import Follow
from users.models import CustomUser
from core.enums import Tuples, UrlRequests

from djoser.views import UserViewSet as DjoserUserViewSet
from django.shortcuts import get_object_or_404
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import F, Q, Sum, Prefetch
from django.http.response import HttpResponse
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
)


class UserViewSet(DjoserUserViewSet, CreateDelViewMixin):
    """Для работы с моделью User.
    Доступен функционал:
    - Вывод пользователей;
    - Регистрация новых пользователей;
    - Оформление/удаление подписки (метод subscribe);
    - Вывод списка подписок (метод subscriptions).
    """
    pagination_class = PageLimitPagination
    add_serializer = UserSubscribeSerializer
    permission_classes = [DjangoModelPermissions]

    @action(
        methods=["post", "delete"],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request: WSGIRequest, id) -> Response:
        """Создание и удаление подписки.
        Метод проверят авторизацию пользователя и
        подписку на собственный аккаунт.
        """
        return self.create_del_obj(id, Follow, Q(author__id=id))

    @action(methods=["get"],detail=False)
    def subscriptions(self, request: WSGIRequest) -> Response:
        """Вывод списка подписчиков.
        Метод проверят авторизацию пользователя.
        """
        if self.request.user.is_anonymous:
            return Response(status=HTTP_401_UNAUTHORIZED)

        pages = self.paginate_queryset(
            CustomUser.objects.filter(subscribers__user=self.request.user)
        )
        serializer = UserSubscribeSerializer(pages, many=True)
        return self.get_paginated_response(serializer.data)
    

class TagViewSet(ReadOnlyModelViewSet): 
    """Для работы с моделью Tag. 
    Изменения доступны только администратору. 
    """ 
    queryset = Tag.objects.all() 
    serializer_class = TagSerializer 
    permission_classes = [AdminOrReadOnly] 
 
 
class IngredientViewSet(ReadOnlyModelViewSet): 
    """Для работы с моделью Ingredient. 
    Изменения доступны только администратору. 
    """ 
    queryset = Ingredient.objects.all() 
    serializer_class = IngredientSerializer 
    permission_classes = [AdminOrReadOnly] 


class RecipeViewSet(ModelViewSet, CreateDelViewMixin):
    queryset = Recipe.objects.select_related('author').order_by('-pub_date',)
    serializer_class = RecipeSerializer
    permission_classes = [AuthorStaffOrReadOnly]
    add_serializer = CropRecipeSerializer
    pagination_class = PageLimitPagination
    ordering_fields = ('pub_date')
    ordering = ('-pub_date',)

    def get_queryset(self):
        """Получает queryset в соответствии с запросом.
        """
        queryset = Recipe.objects.select_related('author')

        tags = self.request.query_params.getlist(UrlRequests.TAGS.value)
        if tags:
            queryset = queryset.filter(tags__slug__in=tags).distinct()

        author = self.request.query_params.get(UrlRequests.AUTHOR.value)
        if author:
            queryset = queryset.filter(author=author)

        if self.request.user.is_anonymous:
            return queryset

        is_in_cart = self.request.query_params.get(UrlRequests.SHOP_CART)
        if is_in_cart in Tuples.SYMBOL_TRUE_SEARCH.value:
            queryset = queryset.filter(
                in_shopping_cart__user=self.request.user
            )
        elif is_in_cart in Tuples.SYMBOL_FALSE_SEARCH.value:
            queryset = queryset.exclude(
                in_shopping_cart__user=self.request.user
            )
        is_favorit = self.request.query_params.get(UrlRequests.FAVORIT)
        if is_favorit in Tuples.SYMBOL_TRUE_SEARCH.value:
            queryset = queryset.filter(in_favorites__user=self.request.user)
        if is_favorit in Tuples.SYMBOL_FALSE_SEARCH.value:
            queryset = queryset.exclude(in_favorites__user=self.request.user)
        return queryset.order_by('-pub_date',)

    @action(
        methods=["get", "post", "delete"],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request: WSGIRequest, pk: int | str) -> Response:
        """Вывод списка 'избранное'.
        Удаление и добавление в избранное.
        """
        return self.create_del_obj(pk, Favorit, Q(recipe__id=pk))

    @action(
        methods=["get", "post", "delete"],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request: WSGIRequest, pk: int | str) -> Response:
        """Вывод списка из корзины.
        Удаление и добавление из корзины.
        """
        return self.create_del_obj(pk, Cart, Q(recipe__id=pk))

    @action(methods=("get",), detail=False)
    def download_shopping_cart(self, request: WSGIRequest) -> Response:
        """Загрузка списка ингридиентов."""
        user = self.request.user
        if not user.carts.exists():
            return Response(status=HTTP_400_BAD_REQUEST)

        filename = f"{user.username}_shopping_list.txt"
        shopping_list = [f"Ваш список покупок:\n\n{user.first_name}\n"]
        ingredients = Ingredient.objects.filter(
            recipe__recipe__in_shopping_cart__user=user
        ).values(
            'name',
            measurement=F('measurement_unit')
        ).annotate(amount=Sum('recipe__amount'))

        for ing in ingredients:
            shopping_list.append(
                f'{ing["name"]}: {ing["amount"]} {ing["measurement"]}'
            )
        shopping_list = '\n'.join(shopping_list)
        response = HttpResponse(
            shopping_list,
            content_type="text.txt; charset=utf-8"
        )

        response["Content-Disposition"] = f"attachment; filename={filename}"
        return response
