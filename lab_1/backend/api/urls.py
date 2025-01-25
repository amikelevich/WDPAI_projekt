from django.urls import path
from .views import (
    CurrentUserView, business_user_list, business_user_detail, create_campaign, list_campaigns, delete_campaign, update_campaign,
    register, system_user_detail
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="Dokumentacja API aplikacji do tworzenia zbiórek charytatywnych",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="kontakt@twojemail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


#endpointy zgodne z poleceniem w wordzie.
urlpatterns = [
    # BusinessUser endpointy - logika biznesowa
    path('business-users/', business_user_list, name='business_user_list'),  # GET, POST
    path('business-users/<int:id>/', business_user_detail, name='business_user_detail'),  # GET, PUT, DELETE

    # SystemUser endpointy - Logowanie i Rejestracjs
    # TokenObtainPairView dziala tak, ze zwraca dwa tokeny JWT gdy istnieje w bazie ludek, jak nie to 401 Unauthorized
    # Domyślnie on sobie patrzy po SystemUser, ponieważ mamy w opcjach go ustawionego jako default.
    path('register/', register, name='register'),  # POST - rejestracja
    path('login/', TokenObtainPairView.as_view(), name='login'),  # POST - login
    path('me/', system_user_detail, name='system_user_detail'),  # GET - info o uzytkowniku
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('user/', CurrentUserView.as_view(), name='current_user'),
    path('campaigns/', list_campaigns, name='list_campaigns'),
    path('campaigns/create/', create_campaign, name='create_campaign'),
    path('campaigns/delete/<int:id>/', delete_campaign, name='delete_campaign'),
    path('campaigns/update/<int:id>/', update_campaign, name='update_campaign'),
]