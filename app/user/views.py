from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
# import the user serializer that we created
from user.serializers import UserSerializer, AuthTokenSerializer


# use the create api view from django
class CreateUserView(generics.CreateAPIView):
    """
    Create a new user in the system
    https://www.django-rest-framework.org/api-guide/generic-views/#createapiview
    """
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES