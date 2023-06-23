from django.contrib import admin
from .models import Account, User, License_Plate, Parking_History
# Register your models here.
admin.site.register(Account)
admin.site.register(User)
admin.site.register(License_Plate)
admin.site.register(Parking_History)