# from django.db import models
# from django.contrib.auth.models import AbstractUser

# class User(AbstractUser):
#     email = models.EmailField(unique=True)

#     def __str__(self) -> str:
#         return self.email

#     def save(self, **kwargs) -> "User":
#         self.username = self.email
#         return super().save(**kwargs)