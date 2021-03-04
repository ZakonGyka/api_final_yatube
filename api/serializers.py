from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Comment, Post, Follow, User, Group


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    # title = serializers.ReadOnlyField()
    # slug = serializers.SlugRelatedField(slug_field='username',
    #                                     read_only=True
    #                                     )
    class Meta:
        fields = '__all__'
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username',
                                        read_only=True,
                                        default=serializers.CurrentUserDefault
                                        )
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True,
                                          queryset=User.objects.all()
                                          )

    # def validate(self, data):
    #     if data['user'] == data['author']:
    #         raise serializers.ValidationError(
    #             'Нельзя подписаться на самого себя!!!'
    #         )
    #     return data

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