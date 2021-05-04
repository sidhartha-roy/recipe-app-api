# This is where the serializers for the user are stored
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


# create a new class called UserSerializer which is
# going to be inherited from the model serializer
# Django has a serializer that we can build from. This
# can perform the database conversion for us and even
# helps us with creating and retrieving from the database.
class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        # get_user_model returns the User model Class
        model = get_user_model()
        # specify the fields that you want to include the serializer
        # these are the fields that are going to be converted to and from
        # JSON when we make our http POST request and we retrieve it in our
        # view and save it to a model.
        # These are the fields that we want to make accessible in our API
        # either to read or write

        # these are the 3 fields we are going to accept when we create an user
        # if we wanted to create a new user field we can add it here.
        fields = ('email', 'password', 'name')

        # This allows us to add a few extra settings in our model serializer
        # To ensure that the password is right only if the minimal chars is 5.
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """
        Create a new user with encrypted password and return it
        see django doc:
        https://www.django-rest-framework.org/api-guide/serializers/#modelserializer
        The doc specifies all the available functions that we can override in
        different serializers
        """
        # the validated data will be the JSON data
        # that is passed in the http POST
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = ('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user

        return attrs
