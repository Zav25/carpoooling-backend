from rest_framework import viewsets, permissions
from .models import User, Ride, Vehicle
from .serializers import UserSerializer, RideSerializer, VehicleSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class VehicleViewSet(viewsets.ModelViewSet):
    """
    This viewset provides `list`, `create`, `retrieve`, `update`, and `destroy` actions for vehicles.
    """
    queryset = Vehicle.objects.all()  # Define the queryset for the viewset
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticated]  # Ensure the user is authenticated

    def perform_create(self, serializer):
        """
        Automatically set the owner to the current logged-in user when creating a vehicle.
        """
        serializer.save(owner=self.request.user)

class RideViewSet(viewsets.ModelViewSet):
    """
    This viewset provides `list`, `create`, `retrieve`, `update`, and `destroy` actions.
    The logged-in user is set as the driver when creating a ride.
    """
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [permissions.IsAuthenticated]  # Ensure the user is authenticated

    def perform_create(self, serializer):
        """
        Automatically set the driver to the current logged-in user when creating a ride.
        """
        serializer.save(driver=self.request.user)



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
