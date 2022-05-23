from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from api.pagination import PagePagination
from users.serializers import CustomUserSerializer
from users.models import CustomUserCreate, Follow
from users.serializers import FollowListSerializer
from djoser.views import UserViewSet
from api import response_messages as msg

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = PagePagination
    permission_classes = (AllowAny,)

    @action(detail=False, permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        subscriptions = self.request.user.follower.all()
        pages = self.paginate_queryset(subscriptions)
        if pages is not None:
            serializer = FollowListSerializer(
                instance=pages, many=True,
                context={'request': request}
            )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True, methods=('post', 'delete',),
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, id):
        following = get_object_or_404(User, id=id)
        subscription = self.request.user.follower.filter(following=following)
        if request.method == 'POST':
            if subscription.exists():
                return Response(
                    msg.SUBSCRIPTION_ERROR,
                    status=status.HTTP_400_BAD_REQUEST
                )
            elif following == self.request.user:
                return Response(
                    msg.SELF_SUBSCRIPTION_ERROR,
                    status=status.HTTP_400_BAD_REQUEST
                )

            subscription = Follow.objects.create(
                user=self.request.user, following=following
            )
            serializer = FollowListSerializer(subscription)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        if request.method == 'DELETE':
            if subscription.exists():
                subscription.delete()
                return Response(
                    msg.UNSUBSCRIBE_INFO,
                    status=status.HTTP_204_NO_CONTENT
                )

            return Response(
                msg.UNSUBSCRIBE_ERROR,
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_403_FORBIDDEN)

    @action(
        methods=["get"],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path="me",
        url_name="me",
    )
    def me(self, request, *args, **kwargs):
        if request.method == "GET":
            me = self.request.user
            serializer = self.get_serializer(me)
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK,
                content_type="application/json",
            )
        return None


# class FollowApiView(APIView):
#     pagination_class = PagePagination
#     filter_backends = [DjangoFilterBackend]
#     permission_classes = [IsAuthenticated]

#     @action(detail=True, methods=['post', ],)
#     def post(self, request, id):
#         data = {'user': request.user.id, 'following': id}
#         serializer = FollowSerializer(data=data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def delete(self, request, id):
#         user = request.user
#         following = get_object_or_404(CustomUserCreate, id=id)
#         follow = get_object_or_404(
#             Follow, user=user, following=following
#         )
#         follow.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class FollowListAPIView(ListAPIView):
#     pagination_class = PagePagination
#     filter_backends = [DjangoFilterBackend]
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         queryset = CustomUserCreate.objects.filter(following__user=user)
#         page = self.paginate_queryset(queryset)
#         serializer = FollowListSerializer(
#             page, many=True,
#             context={'request': request}
#         )
#         return self.get_paginated_response(serializer.data)
