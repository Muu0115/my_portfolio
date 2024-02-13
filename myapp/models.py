from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from datetime import datetime
from django.utils import timezone
from datetime import date
#from .models import WebLink  
#from .models import GuestBookEntry  
#from django.core.validators import URLValidator

User = get_user_model()

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)

class UserCredentials(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    password_hash = models.CharField(max_length=128)

    # 他に必要なフィールドがあれば追加

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

class SessionTokens(models.Model):
    token_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    expiry_date = models.DateTimeField()

def __str__(self):
        return f"Token: {self.token} - User: {self.user.username}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    target = models.CharField(max_length=255, default="未設定")  # ユーザーの目標を保存するフィールド
    height = models.FloatField(null=True, blank=True)  # 身長（メートル単位）
    weight = models.FloatField(null=True, blank=True)  # 体重（キログラム単位）
    exercise_goal = models.TextField(null=True, blank=True)  # 運動目標


    def calculate_bmi(self):
        if self.height and self.weight:
            return self.weight / (self.height ** 2)
        return None

class HealthRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    sleep_hours = models.DecimalField(max_digits=4, decimal_places=1)
    CONDITION_CHOICES = [(i, str(i)) for i in range(1, 6)]
    physical_condition = models.IntegerField(choices=CONDITION_CHOICES)
    stress_level = models.IntegerField(choices=CONDITION_CHOICES)
    hydration_amount = models.IntegerField()
    breakfast_content = models.TextField(blank=True, null=True)  # 朝食内容
    lunch_content = models.TextField(blank=True, null=True)      # 昼食内容
    dinner_content = models.TextField(blank=True, null=True)     # 夕食内容
    other_meal_content = models.TextField(blank=True, null=True) # その他の食事内容
    training_content = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Health Record for {self.user.get_username()} on {self.date}"
    
class WebLink(models.Model):
    # 既存のフィールド
    title = models.CharField(max_length=255)
    url = models.URLField()
    description = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    purpose = models.CharField(max_length=255, blank=True)  # 動画の目的や用途
    tags = models.CharField(max_length=255, blank=True)     # 動画に関連するタグ

    def __str__(self):
        return f"{self.title} - {self.purpose}"


class GuestBookEntry(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    description = models.TextField()

class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)  # 追加

class Reply(models.Model):
    entry = models.ForeignKey(Entry, related_name='replies', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

class DailyWeight(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    weight = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ('user', 'date')