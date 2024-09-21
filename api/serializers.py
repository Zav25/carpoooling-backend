from rest_framework import serializers
from .models import User, Vehicle, Ride

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Include all fields of the User model
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'is_driver', 'phone_number', 'nid_passport', 'address']
        extra_kwargs = {
            'password': {'write_only': True}  # Password will not be read in responses
        }

    def create(self, validated_data):
        """
        Overriding the create method to handle password hashing
        """
        # Remove password from validated_data to avoid it being handled as plain text
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # Use set_password to hash the password
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Overriding the update method to handle password updates
        """
        # If password is being updated, hash it first
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)
        instance.save()
        return instance
    
class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        # Include all fields of the Vehicle model
        fields = ['id', 'owner', 'license_plate', 'model', 'capacity']
        # Make sure 'owner' is read-only, as it's set when the vehicle is created
        extra_kwargs = {
            'owner': {'read_only': True}
        }

    def create(self, validated_data):
        """
        Overriding create method to automatically set the vehicle's owner
        """
        # 'owner' should be passed from the request context (e.g., the logged-in user)
        request = self.context.get('request')
        owner = request.user
        vehicle = Vehicle.objects.create(owner=owner, **validated_data)
        return vehicle

class RideSerializer(serializers.ModelSerializer):
    driver = serializers.ReadOnlyField(source='driver.username')  # Read-only driver username
    passenger = serializers.SlugRelatedField(
        queryset=User.objects.all(), 
        slug_field='username', 
        required=False  # Make this optional for ride creation
    )

    class Meta:
        model = Ride
        fields = ['id', 'driver', 'passenger', 'origin', 'destination', 'start_time', 'end_time', 'price']

    def create(self, validated_data):
        ride = Ride.objects.create(driver=self.context['request'].user, **validated_data)
        return ride