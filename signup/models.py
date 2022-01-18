from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .formatChecker import ContentTypeRestrictedFileField
from django.core.validators import FileExtensionValidator
# Create your models here.

# Create your models here.
class UserProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    last_otp = models.IntegerField(default=0)
    secret_string=models.CharField(max_length=100)
    otp_count= models.IntegerField(default=0)
    address = models.CharField(max_length=1000)

    def __str__(self): 
        return self.user.username






class seller(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, blank=True, null=True)
    pdf = ContentTypeRestrictedFileField(upload_to='pdf/',content_types=['application/pdf'],max_upload_size=5242880,blank=True, null=True)
    #pdf=models.FileField(upload_to='pdf/',validators=[FileExtensionValidator(['pdf'])])
    # validate_file = FileValidator(max_size=1024 * 100, content_types=('application/pdf',))
    # pdf = models.FileField(upload_to='pdf/', validators=[validate_file])
    def __str__(self): 
        return self.user.username


class Admin(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self): 
        return self.user.username
