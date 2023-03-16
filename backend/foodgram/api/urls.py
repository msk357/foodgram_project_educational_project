from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet, TagViewSet, IngredientViewSet, RecipeViewSet

app_name = "api"

router = DefaultRouter()
router.register("tags", TagViewSet, "tags")
router.register("ingredients", IngredientViewSet, "ingredients")
router.register("users", UserViewSet, "users")
router.register("recipes", RecipeViewSet, "recipes")

urlpatterns = (
    path("", include(router.urls)),
    path("auth/", include("djoser.urls.authtoken")),
)
