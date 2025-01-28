from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUserManager(BaseUserManager):
    """
    Custom manager for the CustomUser model with no username field.
    Email is the unique identifier for authentication.
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)  # Users are active by default
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)
    


class CustomUser(AbstractUser):
    # Remove the username field, use email as the unique identifier
    username = None
    email = models.EmailField(unique=True)  # Use email as the unique identifier
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    user_type = models.CharField(
        max_length=10,
        choices=[
            ('normal', 'Normal User'),
            ('agent', 'Agent'),
        ],
        default='normal'
    )
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    eth_address = models.CharField(max_length=42, blank=True, null=True)  # Ethereum address

    def get_profile_picture_url(self):
        if self.profile_picture:
            return self.profile_picture.url
        return '/static/assets/assets/images/profile/default.jpg'


    # Assign the custom manager
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Other fields required when creating a superuser

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_agent(self):
        return self.user_type == 'agent'
    
    
class Property(models.Model):
    agent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='leased_properties')
    house_image = models.ImageField(upload_to='house_images/')
    house_video = models.FileField(upload_to='house_videos/', blank=True, null=True)
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    details = models.TextField()
    title = models.CharField(max_length=255)  # Added Title field
    beds = models.IntegerField()  # Added Beds field
    bath = models.IntegerField()  # Added Bath field
    garage = models.IntegerField()  # Added Garage field
    area = models.DecimalField(max_digits=10, decimal_places=2)  # Added Area field (in square meters or feet)
    date_leased = models.DateTimeField(auto_now_add=True)
    is_rented = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.location} - {self.agent.first_name} {self.agent.last_name}"




class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='house_images/')

    def __str__(self):
        return f"Image for {self.property.title}"