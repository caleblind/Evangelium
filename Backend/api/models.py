from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    tag_name = models.CharField(max_length=100)
    tag_is_predefined = models.BooleanField(default=False)

    def __str__(self):
        return self.tag_name

class Profile(models.Model):
    USER_TYPES = (
        ('Missionary', 'Missionary'),
        ('Church', 'Church'),
        ('Supporter', 'Supporter'),
    )

    DENOMINATIONS = (
        ('Baptist', 'Baptist'),
        ('Catholic', 'Catholic'),
        ('Protestant', 'Protestant'),
        ('Non-Denominational', 'Non-Denominational'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    denomination = models.CharField(max_length=50, choices=DENOMINATIONS, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user_type})" 