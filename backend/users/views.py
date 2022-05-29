from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api import messages
from api.pagination import PagePagination
from users.models import Follow
from users.serializers import CustomUserSerializer, FollowListSerializer

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
                    messages.SUBSCRIPTION_ERROR,
                    status=status.HTTP_400_BAD_REQUEST
                )
            elif following == self.request.user:
                return Response(
                    messages.SELF_SUBSCRIPTION_ERROR,
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
                    messages.UNSUBSCRIBE_INFO,
                    status=status.HTTP_204_NO_CONTENT
                )

            return Response(
                messages.UNSUBSCRIBE_ERROR,
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
