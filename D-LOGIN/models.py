from django.db import models

# Create your models here.

class account(models.Model): # < Account database model
    Username = models.CharField(max_length=255, blank=False) # < Username column
    Password = models.CharField(max_length=255, blank=False) # < Password column

    def __str__(self):
        AC = f"{self.Username} {self.Password}" # < What will show
        return AC

class information(models.Model):
    User = models.CharField(max_length=255, blank=False)
    Info = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return self.Info