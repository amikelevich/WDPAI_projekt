from rest_framework import serializers
from .models import BusinessUser, Campaign
from .models import SystemUser
import base64

#Taki łącznik między requestami a bazą danych, zmienia dane modelu np z pythona na Jsona oraz odwrotnie, transferuje z bazy do backendu i odwrotnie
class BusinessUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessUser
        fields = ['id', 'first_name', 'last_name', 'role']

# Serializery dla SystemUser
class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer do rejestracji użytkownika systemowego.
    """
    password = serializers.CharField(write_only=True)  #zadbaj by to pole było jedynie do odczytu
    class Meta:
        model = SystemUser
        fields = ['username', 'email', 'password']  # Pola wymagane do rejestracji

    def create(self, validated_data):
        user = SystemUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer do odczytu danych użytkownika systemowego.
    """
    class Meta:
        model = SystemUser
        fields = ['id', 'username', 'email'] 

class CampaignSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField() # odczytuje obraz z bazy danych i koduje go w formacie Base64
    image_upload = serializers.CharField(write_only=True, required=False)  # przyjmuje obraz w formacie Base64 i przekształca go do formatu binarnego i wrzuca do bazy

    class Meta:
        model = Campaign
        fields = ['campaign_id', 'name', 'description', 'target_amount', 'raised_amount', 'status', 'image', 'image_upload']
    
    # zmieniam obraz na ten typ z biblioteki i zwracam jako odpowiedź
    def get_image(self, obj):
        if obj.image:
            return base64.b64encode(obj.image).decode('utf-8')
        return None

    # dekodujemy obraz oraz tworzymy rekord
    def create(self, validated_data):
        image_upload = validated_data.pop('image_upload', None)
        if image_upload:
            validated_data['image'] = base64.b64decode(image_upload)
        return super().create(validated_data)