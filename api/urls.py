from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView
from .views import  CustomTokenObtainPairView, UserViewSet, RideViewSet, VehicleViewSet, SignInView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'rides', RideViewSet)
router.register(r'vehicles', VehicleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signin/', SignInView.as_view(), name='signin'),
]


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns += [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


# need to add signin and signup