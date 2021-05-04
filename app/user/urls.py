# this allows us to define different paths in our app
from django.urls import path

from user import views


# the name of the app we are creating the url for
app_name = 'user'

# the path function is used to create a new path
# we used create here because we want the path to be
# users/create for create_user
# Also, remember to update the url in the main app url
urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me')
]
