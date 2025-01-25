from rest_framework import serializers
from .models import BusinessUser, Campaign
from .models import SystemUser


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
    class Meta:
        model = Campaign
        fields = ['campaign_id', 'name', 'description', 'target_amount', 'raised_amount', 'status']

    def update(self, instance, validated_data):
        donation_amount = validated_data.get('donation_amount', 0)
        if donation_amount > 0:
            instance.raised_amount += donation_amount
        instance.save()
        return instance
