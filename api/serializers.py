from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Comment, Post, Follow, User


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True
                                          )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username',
                                        read_only=True
                                        )
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True,
                                          queryset=User.objects.all()
                                          )

    def validate(self, data):
        if data['user'] == data['author']:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!!!'
            )
        return data

    class Meta:
        fields = '__all__'
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'author'],
                message='Нельзя подписаться на самого себя!',
            )
        ]