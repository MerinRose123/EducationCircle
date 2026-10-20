import binascii
import os
from io import BytesIO
from PIL import Image

from django.db.models import Q
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.files import File


from common.models import BaseModel
from django.contrib.auth.models import UserManager


def compress(image):
    im = Image.open(image)
    # create a BytesIO object
    im_io = BytesIO() 
    # save image to BytesIO object
    im.save(im_io, 'JPEG', quality=10) 
    # create a django-friendly Files object
    new_image = File(im_io, name=image.name)
    return new_image


class User(AbstractBaseUser, PermissionsMixin,BaseModel):
    # User Properties
    username = models.CharField(_('Display Name'), max_length=50, default='') # Used as display name
    first_name = models.CharField(_('First Name'), max_length=50, default='', blank=True)
    last_name = models.CharField(_('Last Name'), max_length=50, default='', blank=True)
    email = models.EmailField(_('Email Address'), max_length=255, unique=True)
    phone_number = models.CharField(_('Phone Number'), max_length=12, blank=True, default='')
    address = models.CharField(_('Address'), max_length=150, default='', blank=True)
    profile_image = models.ImageField(_('Profile Image'),blank=True, null=True, upload_to='images/')


    # For admin side access
    is_staff = models.BooleanField(default=False)

    # Company Admin
    is_company_admin = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()
    
    # TODO : Add saved questions and send notifications flag
    
    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # call the compress function if image is uploaded
        if self.profile_image:
            new_image = compress(self.profile_image)
            # set self.image to new_image
            self.profile_image = new_image

        # save
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"





