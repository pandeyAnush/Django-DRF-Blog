from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        if User.objects.filter(username=data['username'].lower()).exists():
            raise serializers.ValidationError('Username is taken')
        return data

    def create(self, validated_data):
        user = User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'].lower()
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()  # Save the user object
        return validated_data

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        if not User.objects.filter(username=data['username'].lower()).exists():
            print(f"User with username {data['username']} does not exist.")
            raise serializers.ValidationError('Account Not Found')
        return data    

    def get_jwt_token(self, data):
        # Convert username to lowercase for authentication
        user = authenticate(
            request=self.context.get('request'),
            username=data['username'].lower(),
            password=data['password']
        )

        if not user:
            print(f"Authentication failed for user: {data['username']}")
            return {'message': 'Invalid Credentials', 'data': {}}

        print(f"User {user.username} successfully authenticated.")
        refresh = RefreshToken.for_user(user)

        return {
            'message': 'Successfully logged in',
            'data': {
                'token': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }
        }
