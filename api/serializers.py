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
    # Override the owner field to show only users who are drivers
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(is_driver=True))

    class Meta:
        model = Vehicle
        fields = ['id', 'owner', 'license_plate', 'model', 'capacity']

    def create(self, validated_data):
        """
        Override the create method to handle vehicle creation.
        """
        vehicle = Vehicle.objects.create(**validated_data)
        return vehicle

class RideSerializer(serializers.ModelSerializer):
    # Filter drivers for the 'driver' field (users who have is_driver=True)
    driver = serializers.SlugRelatedField(
        queryset=User.objects.filter(is_driver=True),  # Only users who are drivers
        slug_field='username',
        required=True  # Make this required for ride creation
    )

    # Filter passengers for the 'passenger' field (users who have is_driver=False)
    passenger = serializers.SlugRelatedField(
        queryset=User.objects.filter(is_driver=False),  # Only users who are not drivers
        slug_field='username',
        allow_null=True,  # Allow passenger to be null
        required=False
    )

    class Meta:
        model = Ride
        fields = ['id', 'driver', 'passenger', 'origin', 'destination', 'num_persons', 'start_time', 'end_time', 'price', 'status']
        read_only_fields = ['status']  # Make 'status' read-only by default

    def create(self, validated_data):
        # Use the driver from validated_data to create the ride
        ride = Ride.objects.create(**validated_data)
        return ride

    def to_representation(self, instance):
        """ Customize the representation of the ride instance to include driver and passenger info """
        representation = super().to_representation(instance)
        representation['driver'] = instance.driver.username if instance.driver else None
        representation['passenger'] = instance.passenger.username if instance.passenger else None
        return representation
