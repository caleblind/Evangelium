# Generated by Django 4.2.16 on 2024-11-12 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseApp', '0004_user_groups_user_user_permissions'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
