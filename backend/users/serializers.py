from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from ingredients_recipes.models import Recipe
from users.models import CustomUserCreate, Follow
from api import response_messages as msg


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

# class CustomUserSerializer(UserSerializer):
#     is_subscribed = serializers.SerializerMethodField()

#     class Meta:
#         model = User
#         fields = (
#             'email', 'id', 'username', 'first_name', 'last_name',
#             'is_subscribed',
#         )

#     def get_is_subscribed(self, obj):
#         request = self.context.get('request')
#         if request is None:
#             return False
#         if request.user.is_anonymous:
#             return False

#         return request.user.follower.filter(author=obj.id).exists()




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
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following'],
                message=(msg.SUBSCRIPTION_ERROR)
            )
        ]

    def validate_id(self, value):
        if self.context['request'].user.id == value:
            raise serializers.ValidationError(msg.SELF_SUBSCRIPTION_ERROR)
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




# class FollowSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Follow
#         fields = ('user', 'following')
#         validators = [
#             UniqueTogetherValidator(
#                 queryset=Follow.objects.all(),
#                 fields=('user', 'following'),
#                 message=('Вы уже подписаны на этого юзера!')
#             )
#         ]

#     def to_representation(self, instance):
#         request = self.context.get('request')
#         context = {'request': request}
#         return FollowListSerializer(
#             instance.following, context=context).data

#     def validate(self, data):
#         request = self.context.get('request')
#         if not request or request.user.is_anonymous:
#             return False
#         following = data['following']
#         if request.user == following:
#             raise serializers.ValidationError(
#                 'Подписаться на самого себя невозможно!'
#             )
#         return data


    # class Meta:
    #     model = CustomUserCreate
    #     fields = ('email', 'id', 'username', 'first_name', 'last_name',
    #               'is_subscribed', 'recipes', 'recipes_count')

    # def get_is_subscribed(self, obj):
    #     request = self.context.get('request')
    #     if not request or request.user.is_anonymous:
    #         return False
    #     return Follow.objects.filter(user=request.user, following=obj).exists()

    # def get_recipes(self, obj):
    #     request = self.context.get('request')
    #     if not request or request.user.is_anonymous:
    #         return False
    #     context = {'request': request}
    #     recipes_limit = request.query_params.get('recipes_limit')
    #     if recipes_limit is not None:
    #         recipes = obj.recipes.all()[:int(recipes_limit)]
    #     else:
    #         recipes = obj.recipes.all()
    #     return FollowRecipesSerializer(
    #         recipes, many=True, context=context).data

    # def get_recipes_count(self, obj):
    #     return Recipe.objects.filter(author=obj.author).count()
