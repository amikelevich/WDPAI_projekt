from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
#Tworzy model usera, który pojawi się potem w naszej bazie danych - django tworzy tabelę na bazie tego modelu, definiujemy typy i długości
#__str__ pozwala zwracać dane w pewnej formie - reprezentacja pod printa
class BusinessUser(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=50)

    def __str__(self):
       return f'{self.first_name} {self.last_name} - {self.role}'
#podobno jest jakiś defaultowy user, którego rozszerzamy o kolejne pola.    
class SystemUser(AbstractUser):
    """
    Systemowy użytkownik odpowiedzialny za logowanie i rejestrację.
    """
    email = models.EmailField(unique=True) # zadbaj by wymagana była unikalność
    groups = models.ManyToManyField( #jakaś relacja wiele do wielu z grupami 
        Group,
        related_name="custom_user_set", 
        blank=True,
    )
    user_permissions = models.ManyToManyField( #jakaś relacja wiele do wielu z permisjami 
        Permission,
        related_name="custom_user_permissions_set",  
        blank=True,
    )
    
class Campaign(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
    ]

    campaign_id = models.AutoField(primary_key=True) 
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True) 
    target_amount = models.DecimalField(max_digits=10, decimal_places=2) 
    raised_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return self.name