from django.urls import path
from .views import home, signup, user_login, logout_user, add_country, remove_country

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', logout_user, name='logout'),
    path('add-country/', add_country, name='add_country'),
    path('remove-country/<int:country_id>/', remove_country, name='remove_country'),
]
