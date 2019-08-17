from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipe

from recipe import serializers


class BaseRecipeAttr(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin):
    """Base viewset for user owned recipe attributes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes  = (IsAuthenticated,)

    def get_queryset(self):
        """Return object of the current authenticated object only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttr):
    """Manage tags in the database"""

    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseRecipeAttr):
    """Manage ingredients in the database"""

    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage Recipe in the Database"""
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve the recipe foe authenticated user"""
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new Recipe"""
        serializer.save(user=self.request.user)














