from django.urls import path, include
from rest_framework.authtoken import views
from .views import PostViewSet, CommentViewSet, GroupViewSet, FollowViewSet

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView,
                                            )

v1_router = DefaultRouter()

v1_router.register(r'v1/posts',
                   PostViewSet,
                   basename='post'
                   )
v1_router.register(r'v1/posts/(?P<post_id>\d+)/comments',
                   CommentViewSet,
                   basename='comments'
                   )
v1_router.register(r'v1/group/',
                   GroupViewSet,
                   basename='group'
                   )
v1_router.register(r'v1/follow/',
                   FollowViewSet,
                   basename='follow'
                   )

urlpatterns = [
    path('', include(v1_router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
    path('token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
]
