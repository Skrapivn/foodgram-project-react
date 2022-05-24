from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api import messages
from ingredients_recipes.models import Recipe
from users.models import CustomUserCreate, Follow


class CustomUserCreateSerializer(UserCreateSerializer):  ####
    class Meta:
        model = CustomUserCreate
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'password')


class CustomUserSerializer(UserSerializer):  ####################
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


class FollowRecipesSerializer(serializers.ModelSerializer): #######
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowListSerializer(serializers.ModelSerializer): #####
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
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following'],
                message=(messages.SUBSCRIPTION_ERROR)  # есть проверка во views
            )
        ]

    def validate_id(self, value): # есть проверка во views
        if self.context['request'].user.id == value:
            raise serializers.ValidationError(messages.SELF_SUBSCRIPTION_ERROR)
        return value

    def get_is_subscribed(self, obj):
        return obj.user.follower.filter(following=obj.following).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        queryset = obj.following.recipes.all()
        if request:
            recipes_limit = request.GET.get('recipes_limit')
            if recipes_limit is not None:
                queryset = queryset[:int(recipes_limit)]
        return [FollowRecipesSerializer(item).data for item in queryset]

    def get_recipes_count(self, obj):
        return obj.following.recipes.count()
