from django.urls import include
from django.urls import path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

from api.views import CommentViewSet
from api.views import FollowViewSet
from api.views import GroupViewSet
from api.views import PostViewSet

v1_router = DefaultRouter()

v1_router.register('posts',
                   PostViewSet,
                   basename='post'
                   )
v1_router.register(r'posts/(?P<post_id>\d+)/comments',
                   CommentViewSet,
                   basename='comments'
                   )
v1_router.register('group',
                   GroupViewSet,
                   basename='group'
                   )
v1_router.register('follow',
                   FollowViewSet,
                   basename='follow'
                   )

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
]
