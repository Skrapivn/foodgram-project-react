from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from ingredients_recipes.models import Recipe
from users.models import CustomUserCreate, Follow

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = CustomUserCreate
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'password')


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUserCreate
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=request.user, following=obj).exists()


class FollowRecipesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowListSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='following.email')
    id = serializers.ReadOnlyField(source='following.id')
    username = serializers.ReadOnlyField(source='following.username')
    first_name = serializers.ReadOnlyField(source='following.first_name')
    last_name = serializers.ReadOnlyField(source='following.last_name')
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Follow
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count',
        )

    def get_is_subscribed(self, obj):
        return obj.user.follower.filter(following=obj.following).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes = obj.following.recipes.all()
        if request:
            limit = request.GET.get('recipes_limit')
            if limit is not None:
                recipes = obj.following.recipes.all()[:(int(limit))]
        context = {'request': request}
        return FollowRecipesSerializer(recipes,
                                       many=True,
                                       context=context).data

    def get_recipes_count(self, obj):
        return obj.following.recipes.count()

# key_a = request.GET['a']


    # def get_recipes(self, obj):
    #     recipes_limit = 0
    #     try:
    #         params = self.context['request'].query_params
    #         recipes_limit = int(params.get('recipes_limit', None))
    #     except (KeyError, TypeError, AttributeError):
    #         pass

    #     recipes = Recipe.objects.filter(author=obj)
    #     if recipes_limit:
    #         recipes = recipes[:recipes_limit]
    #     return RecipeSmallSerializer(recipes, many=True).data