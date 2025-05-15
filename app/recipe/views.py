"""
Views for the recipe API
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Recipe
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs"""
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve recipes for authenticated user"""
        # 로그인한 유저의 레시피만 return
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request"""
        if self.action == 'list':
            # 여기는 모든걸 return 하지 않는 recipe
            return serializers.RecipeSerializer

        # 여기는 recipe detail return
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe"""
        # 현재 로그인 유저가 소유자가 되도록 설정하기 위해서
        serializer.save(user=self.request.user)
        