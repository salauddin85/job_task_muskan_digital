
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
class CustomUserManager(BaseUserManager):
    def create_user(self, user_id, password=None, **extra_fields):
        if not user_id:
            raise ValueError('The User Id must be set')
        
        user = self.model(user_id=user_id, **extra_fields)
        user.set_password(password)  # Use set_password to hash the password
        user.save(using=self._db)
        return user 
    
    def create_superuser(self, user_id, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(user_id, password, **extra_fields)



class CustomUser(AbstractBaseUser):
    user_id = models.CharField(max_length=15, unique=True)
    username = models.CharField(max_length=50, unique=True, blank=True, null=True)
    password = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    # related_admin = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='managed_users')

    objects = CustomUserManager()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['password']  

    def __str__(self) -> str:
        return self.user_id
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin



class Module(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='module')
    # user = models.ManyToManyField(CustomUser, related_name='module')
    name = models.CharField(max_length=100)
    price = models.FloatField(max_length=10)
    description = models.CharField(max_length=100)















# class CustomUser(AbstractBaseUser):
#     mobile_number = models.CharField(max_length=15, unique=True)
#     email = models.EmailField(unique=True, blank=True, null=True)
#     username = models.CharField(max_length=150, unique=True, blank=True, null=True)
#     password = models.CharField(max_length=100)
#     is_admin = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     related_admin = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='managed_users')

#     objects = CustomUserManager()

#     USERNAME_FIELD = 'mobile_number'
#     REQUIRED_FIELDS = ['email', 'password']

#     def __str__(self):
#         return self.mobile_number

#     def has_perm(self, perm, obj=None):
#         return self.is_admin

#     def has_module_perms(self, app_label):
#         return self.is_admin


# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# from django.db import models

# class CustomUserManager(BaseUserManager):
#     def create_user(self, mobile_number, password=None, **extra_fields):
#         if not mobile_number:
#             raise ValueError('The mobile number must be set')
#         user = self.model(mobile_number=mobile_number, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, mobile_number, password=None, **extra_fields):
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault('is_admin', True)
#         extra_fields.setdefault('is_active', True)

#         return self.create_user(mobile_number, password, **extra_fields)
