from django.contrib import admin
from .models import UserProfile
from .models import seller,Admin
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(seller)
admin.site.register(Admin)