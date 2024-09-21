from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, RideViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'rides', RideViewSet)

urlpatterns = [
    path('', include(router.urls)),
]


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns += [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
