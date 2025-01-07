from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser

#Custom user manager to handle user creation 
class UserManager(BaseUserManager):
    """
    manager clss for custom User model.
    Handles the creation of regular users and superusers.
    """
    def create_user(self, email, password=None):
        """
        Creates and returns user with the given email and password.
        """
        if not email:
            raise ValueError("Email is required") #Validation to ensure email is provided
        
        #Normalize the email (lowercase domain part) to maintain consistency
        user = self.model(email=self.normalize_email(email))

        # Set the password for the user(hashed internally by Django)
        user.set_password(password)

        #save the user instance to the database
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None):
        """
        Creates and returns a superuser with the given email and password
        """
        user = self.create_user(email, password) #Use the 'create_user' method to ensure user logic
        user.is_staff = True #Grant superuser staff-level permissions
        user.is_superuser = True # Grant superuser full admin access
        user.save(using=self._db)
        return user
    
# Custom user model for authentication
class User(AbstractUser):
    """
    Custom User modle that replaces Django's default user system with email-based login
    
    """
    email = models.EmailField(unique=True, max_length=100)
    username = models.CharField(unique=False, max_length=50)
    
    #optional bio and profile picture fields with image upload capability for user profiles
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

# Specify email as the field used for authentication instead of username
    USERNAME_FIELD = 'email'

# Define additional fields required when creating a user
    REQUIRED_FIELDS = []

#Use the custom manager for user creation
    objects = UserManager()

    def __str__(self):
        return self.email
    