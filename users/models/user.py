import hashlib
from io import BytesIO

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image, ImageDraw, ImageFont


class UserManager(BaseUserManager):
    def create_user(self, email, name, surname, phone, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        if not name:
            raise ValueError("Name is required")
        if not surname:
            raise ValueError("Surname is required")
        if not phone:
            raise ValueError("Phone is required")

        normalized_email = self.normalize_email(email)
        user = self.model(
            email=normalized_email,
            name=name,
            surname=surname,
            phone=phone,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, name, surname, phone, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields["is_staff"] is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields["is_superuser"] is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(email, name, surname, phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=124)
    surname = models.CharField(max_length=124)
    avatar = models.ImageField(upload_to="users/avatars/", blank=True)
    phone = models.CharField(max_length=12, unique=True)
    github_url = models.URLField(blank=True)
    about = models.TextField(max_length=256, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    favorites = models.ManyToManyField(
        "projects.Project",
        related_name="interested_users",
        blank=True,
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname", "phone"]

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.name} {self.surname}"

    def _pick_avatar_background(self):
        palette = [
            "#6B8E73",
            "#7C90A0",
            "#8D7B68",
            "#7F6A93",
            "#5F8A8B",
            "#8A7E66",
        ]
        source = (self.email or self.name or "user").encode("utf-8")
        color_index = int(hashlib.md5(source).hexdigest(), 16) % len(palette)
        return palette[color_index]

    def _build_avatar_file(self):
        image_size = 128
        avatar_image = Image.new(
            "RGB",
            (image_size, image_size),
            self._pick_avatar_background(),
        )
        canvas = ImageDraw.Draw(avatar_image)

        first_letter = (self.name[:1] if self.name else "U").upper()

        try:
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", 72)
        except OSError:
            font = ImageFont.load_default()

        text_box = canvas.textbbox((0, 0), first_letter, font=font)
        text_width = text_box[2] - text_box[0]
        text_height = text_box[3] - text_box[1]

        text_x = (image_size - text_width) / 2
        text_y = (image_size - text_height) / 2

        canvas.text((text_x, text_y), first_letter, fill="white", font=font)

        binary_stream = BytesIO()
        avatar_image.save(binary_stream, format="PNG")
        file_name = f"avatar_{self.email.replace('@', '_').replace('.', '_')}.png"
        return ContentFile(binary_stream.getvalue(), name=file_name)

    def save(self, *args, **kwargs):
        if not self.avatar:
            self.avatar = self._build_avatar_file()
        super().save(*args, **kwargs)
