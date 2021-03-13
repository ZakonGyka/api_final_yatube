from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.validators import UserIsNotFollowingValidator
from api.models import Comment
from api.models import Follow
from api.models import Group
from api.models import Post
from api.models import User


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(source='author.username')

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(source='author.username')

    class Meta:
        fields = '__all__'
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following'],
                message='Повторная подписка запрещена!',
            ),
            UserIsNotFollowingValidator()
        ]
