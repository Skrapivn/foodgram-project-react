from djoser.serializers import UserCreateSerializer, UserSerializer
from ingredients_recipes.models import Recipe
from rest_framework import serializers
from users.models import CustomUserCreate, Follow


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
        limit = request.query_params.get('recipes_limit')
        if limit is not None:
            recipes = obj.recipes.all()[:(int(limit))]
        recipes = obj.recipes.all()
        context = {'request': request}
        return FollowRecipesSerializer(recipes,
                                       many=True,
                                       context=context).data

    def get_recipes_count(self, obj):
        return obj.following.recipes.count()
