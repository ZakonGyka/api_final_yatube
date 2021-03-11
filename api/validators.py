from rest_framework.exceptions import ValidationError


class UserIsNotFollowingValidator:

    requires_context = True

    def __call__(self, attrs, serializer):
        if attrs['following'] == serializer.context['request'].user:
            raise ValidationError('Нельзя подписаться на самого себя!')
