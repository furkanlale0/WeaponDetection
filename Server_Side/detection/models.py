import os
import uuid
from django.db import models

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User
# ŞU SATIRI YENİ EKLEDİK: Depolama sistemini manuel çağırıyoruz
from django.core.files.storage import FileSystemStorage

# Depolama ayarını burada elle oluşturuyoruz.
# Bu sayede settings.py'de ne yazarsa yazsın, dosyalar 'media' klasörüne zorla kaydedilecek.
fs = FileSystemStorage(location='media/', base_url='/media/')

# Changes uploaded file name
def scramble_uploaded_filename(instance, filename):
    """
    Scramble / uglify the filename of the uploaded file, but keep the files extension (e.g., .jpg or .png)
    :param instance:
    :param filename:
    :return:
    """
    extension = filename.split(".")[-1]
    return "{}.{}".format(uuid.uuid4(), extension)

# Data model
class UploadAlert(models.Model):
    # ŞU KISMI DEĞİŞTİRDİK: storage=fs ekledik.
    # Artık resimler %100 senin bilgisayarına (media klasörüne) kaydedilecek.
    image = models.ImageField("Uploaded image", upload_to=scramble_uploaded_filename, storage=fs)
    user_ID = models.ForeignKey(Token, on_delete=models.CASCADE)
    alert_receiver = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)

# Generate and save a token each time a user is saved in a database
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)