from decimal import ROUND_DOWN, Decimal
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .serializers import CampaignSerializer, RegisterSerializer, UserSerializer, BusinessUserSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from .models import BusinessUser, Campaign
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

User = get_user_model()
#User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpassword')

#===================== BusinessUser =====================
@swagger_auto_schema(
    method='get',
    operation_summary="Get the list of business users",
    operation_description="Pobierz listę użytkowników biznesowych.",
    responses={200: "Lista użytkowników biznesowych", 400: "Nieprawidłowe zapytanie"}
)
@swagger_auto_schema(
    method='post',
    operation_summary="Create a new business user",
    operation_description="Dodaj nowego użytkownika biznesowego.",
    request_body=BusinessUserSerializer,
    responses={201: "Dodano użytkownika", 400: "Nieprawidłowe dane"}
)

@api_view(['GET', 'POST'])
#klasy uprawnień, sprawdzające tokeny i wymagające je.
#token: header.payload.signature - isAuthenticated sprawdza praktycznie wszystko, jakieś obliczenia, hashe itp.
@permission_classes([IsAuthenticated])
def business_user_list(request):
    """
    Lista wszystkich BusinessUser oraz tworzenie nowych.
    """
    if request.method == 'GET':
        business_users = BusinessUser.objects.all()
        serializer = BusinessUserSerializer(business_users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BusinessUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='get',
    operation_summary="Get a specific business user",
    operation_description="Otrzymaj użytkownika.",
    responses={200: "Konkretny użytkownik", 404: "Użytkownik nie znaleziony"}
)
@swagger_auto_schema(
    method='put',
    operation_summary="Update a specific business user",
    operation_description="Zaktualizuj użytkownika.",
    responses={200: "Zaktualizowano", 400: "Nieprawidłowe dane", 404: "Użytkownik nie znaleziony"}
)
@swagger_auto_schema(
    method='delete',
    operation_summary="Delete a specific business user",
    operation_description="Usuń użytkownika.",
    responses={200: "Usunięto", 404: "Użytkownik nie znaleziony"}
)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def business_user_detail(request, id):
    """
    Otrzmanie, update lub usunięcie konkretnego BusinessUser.
    """
    try:
        business_user = BusinessUser.objects.get(id=id)
    except BusinessUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BusinessUserSerializer(business_user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BusinessUserSerializer(business_user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        business_user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# ===================== SUser (Logowanie i Rejestracja) =====================

register_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description="Nazwa użytkownika"),
        'email': openapi.Schema(type=openapi.TYPE_STRING, description="Adres email użytkownika"),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description="Hasło użytkownika (min. 8 znaków)"),
    },
    required=['username', 'email', 'password'],  # Pola wymagane
)

@swagger_auto_schema(
    method='post',
    operation_summary="Register a new user.",
    operation_description="Rejestracja nowego użytkownika.",
    request_body=register_request_schema,
    responses={
        201: openapi.Response(
            description="Pomyślnie zarejestrowano użytkownika.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'username': openapi.Schema(type=openapi.TYPE_STRING, description="Nazwa użytkownika"),
                    'email': openapi.Schema(type=openapi.TYPE_STRING, description="Adres email użytkownika"),
                }
            )
        ),
        400: "Nieprawidłowe dane.",
    }
)

@api_view(['POST'])
@permission_classes([AllowAny])  # Usuwamy wymaganie autoryzacji dla tego endpointu
def register(request):
    """
    Nowy uzytkownik systemowy.
    """
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='get',
    operation_summary="Get data about the authenticated user.",
    operation_description="Otrzymanie danych o samym sobie.",
    responses={200: "Otrzymano."}
)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def system_user_detail(request):
    """
    Otrzymanie danych o konkretnym SystemUser.
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@swagger_auto_schema(
    method='get',
    operation_summary="Retrieve a list of campaigns.",
    operation_description="Get a list of all available campaigns.",
    responses={200: "List of campaigns retrieved successfully."}
)

@api_view(['GET'])
@permission_classes([AllowAny])
def list_campaigns(request):
    campaigns = Campaign.objects.all()
    serializer = CampaignSerializer(campaigns, many=True)
    return Response(serializer.data)

@swagger_auto_schema(
    method='post',
    operation_summary="Create a new campaign",
    operation_description="Creates a new campaign with the provided details",
    request_body=CampaignSerializer,
    responses={
        201: openapi.Response(
            description="Campaign successfully created",
            examples={
                "application/json": {
                    "campaign_id": 1,
                    "name": "Nowa kampania",
                    "description": "Opis mojej kampanii",
                    "target_amount": 10000.0,
                }
            }
        ),
        400: "Invalid data",
    }
)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_campaign(request):
    if request.method == 'POST':
        serializer = CampaignSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
@swagger_auto_schema(
    method='delete',
    operation_summary="Delete a campaign.",
    operation_description="Delete a campaign based on its ID.",
    responses={
        204: "Campaign deleted successfully.",
        404: "Campaign not found."
    },
    operation_id="deleteCampaign",
    parameters=[
        openapi.Parameter(
            'id',
            openapi.IN_PATH,
            description="The ID of the campaign to be deleted.",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ]
)    

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_campaign(request, id):
    try:
        campaign = Campaign.objects.get(campaign_id=id)
    except Campaign.DoesNotExist:
        return Response({'error': 'Campaign not found'}, status=status.HTTP_404_NOT_FOUND)
    
    campaign.delete()
    return Response({'message': 'Campaign deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

@swagger_auto_schema(
    method='put',
    operation_summary="Update a campaign donation.",
    operation_description="Updates the raised amount for a campaign. Validates donation amount and checks if the target is reached.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'donation_amount': openapi.Schema(type=openapi.TYPE_NUMBER, description="Amount donated to the campaign", example=50.00)
        },
    ),
    responses={
        200: openapi.Response(
            description="Successfully updated the campaign.",
            schema=CampaignSerializer
        ),
        400: "Invalid donation amount or campaign data.",
        404: "Campaign not found.",
    }
)

@api_view(['PUT'])
def update_campaign(request, id):
    try:
        campaign = Campaign.objects.get(campaign_id=id)
    except Campaign.DoesNotExist:
        return Response({'error': 'Campaign not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        donation_amount = Decimal(request.data.get('donation_amount', 0)).quantize(Decimal('0.01'), rounding=ROUND_DOWN)
    except Exception as e:
        return Response({'error': 'Invalid donation amount'}, status=status.HTTP_400_BAD_REQUEST)
    
    if donation_amount <= 0:
        return Response({'error': 'Donation amount must be greater than 0'}, status=status.HTTP_400_BAD_REQUEST)
    
    updated_raised_amount = campaign.raised_amount + donation_amount
    if updated_raised_amount >= campaign.target_amount:
        campaign.raised_amount = campaign.target_amount
        campaign.status = 'completed'
    else:
        campaign.raised_amount = updated_raised_amount
    
    campaign.save()
    serializer = CampaignSerializer(campaign)
    return Response(serializer.data, status=status.HTTP_200_OK)


class CurrentUserView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({'is_admin': request.user.is_superuser})