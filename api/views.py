from django.shortcuts import get_object_or_404
from .models import Post, Comment, Group, Follow
from .permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer, \
    CommentSerializer, GroupSerializer, FollowSerializer
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    filters_backends = [DjangoFilterBackend]
    filterSet_fields = ['group']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        return Comment.objects.filter(post=post)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthorOrReadOnly]


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthorOrReadOnly]
    filters_backends = [filters.SearchFilter]
    search_fields = ['=user__username', '=author__username', ]

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user)
        else:
            serializer.errors
