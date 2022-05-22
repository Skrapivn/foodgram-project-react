from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from api.pagination import PagePagination
from users.models import CustomUserCreate, Follow
from users.serializers import FollowListSerializer, FollowSerializer


class FollowApiView(APIView):
    pagination_class = PagePagination
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post', ],)
    def post(self, request, id):
        data = {'user': request.user.id, 'following': id}
        serializer = FollowSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        user = request.user
        following = get_object_or_404(CustomUserCreate, id=id)
        follow = get_object_or_404(
            Follow, user=user, following=following
        )
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowListAPIView(ListAPIView):
    pagination_class = PagePagination
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        queryset = CustomUserCreate.objects.filter(following__user=user)
        page = self.paginate_queryset(queryset)
        serializer = FollowListSerializer(
            page, many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
