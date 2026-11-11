import random
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from django.core.files.base import ContentFile
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def _create_user(self, email, password, name, surname, phone, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, surname=surname, phone=phone, **extra_fields)
        user.set_password(password)

        # Генерация аватарки с первой буквой имени
        if not user.avatar:
            avatar_file = self.generate_avatar(name)
            user.avatar.save(f"avatar_{email}.png", avatar_file, save=False)

        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, name="", surname="", phone="", **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, name, surname, phone, **extra_fields)

    def create_superuser(self, email, password=None, name="Admin",
                         surname="Admin", phone="+70000000000",
                         **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password, name, surname, phone, **extra_fields)

    def generate_avatar(self, name):
        """Генерирует картинку с первой буквой имени на случайном фоне."""
        color = (random.randint(50, 150), random.randint(50, 150), random.randint(50, 150))
        img = Image.new("RGB", (150, 150), color=color)
        draw = ImageDraw.Draw(img)
        letter = name[0].upper() if name else "U"

        try:
            font = ImageFont.load_default()
        except Exception:
            font = None

        draw.text((55, 45), letter, fill=(255, 255, 255), font=font)
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        return ContentFile(buffer.getvalue())


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=124)
    surname = models.CharField(max_length=124)
    avatar = models.ImageField(upload_to="avatars/")
    phone = models.CharField(max_length=12, unique=True)
    github_url = models.URLField(blank=True, null=True)
    about = models.TextField(max_length=256, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname", "phone"]

    def __str__(self):
        return f"{self.name} {self.surname} ({self.email})"
