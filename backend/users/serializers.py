from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
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
    image = Base64ImageField(max_length=None, use_url=True)

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
        if self.context:
            limit = self.context['request'].GET.get('recipes_limit')
            if limit:
                queryset = Recipe.objects.filter(
                    author=obj.following)[:int(limit)]
        else:
            queryset = Recipe.objects.filter(author=obj.following)
        return FollowRecipesSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return obj.following.recipes.count()
