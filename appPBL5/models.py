from django.db import models

# Create your models here.
class Account(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    isAdmin = models.BooleanField(default=False)
    def __str__(self):
        return self.username
    
class User(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    account = models.OneToOneField(Account, on_delete=models.CASCADE)

class License_Plate(models.Model):
    number_plate = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='license_plates')
    
class Parking_History(models.Model):
    check_in_time = models.DateTimeField()
    check_out_time = models.DateTimeField()
    price = models.IntegerField()
    isPaid = models.BooleanField(default=False)
    license_plate = models.ForeignKey(License_Plate, on_delete=models.CASCADE)
