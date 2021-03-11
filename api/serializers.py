
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from .models import Comment
from .models import Follow
from .models import Group
from .models import Post
from .models import User


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date', 'group')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username',
                                        read_only=True,
                                        default=serializers.CurrentUserDefault()
                                        )
    following = serializers.SlugRelatedField(slug_field='username',
                                             queryset=User.objects.all()
                                             )

    def validate(self, attrs):
        if attrs['following'] == self.context['request'].user:
            raise ValidationError('Нельзя подписаться на самого себя!')
        return attrs

    class Meta:
        fields = '__all__'
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following'],
                message='Повторная подписка запрещена!',
            )
        ]
