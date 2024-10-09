from rest_framework import viewsets, permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .models import User, Ride, Vehicle
from .serializers import UserSerializer, RideSerializer, VehicleSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]

class VehicleViewSet(viewsets.ModelViewSet):
    """
    This viewset provides `list`, `create`, `retrieve`, `update`, and `destroy` actions for vehicles.
    """
    queryset = Vehicle.objects.all()  # Define the queryset for the viewset
    serializer_class = VehicleSerializer
    # permission_classes = [permissions.IsAuthenticated]  # Commented out to disable authentication

    def perform_create(self, serializer):
        """
        Allow owner to be set manually through the request data.
        """
        # No need to set owner from request.user
        serializer.save()

class RideViewSet(viewsets.ModelViewSet):
    """
    This viewset provides `list`, `create`, `retrieve`, `update`, and `destroy` actions.
    """
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    # permission_classes = [permissions.IsAuthenticated]  # Uncomment if authentication is required

    def perform_create(self, serializer):
        # Just call save, no additional driver assignment
        serializer.save()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class SignInView(APIView):
    def post(self, request):
        username = request.data.get('username')  # Get the username from the request
        password = request.data.get('password')  # Get the password from the request

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user is not None:
            # If authentication is successful, return user information
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # If authentication fails, return an error response
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)
