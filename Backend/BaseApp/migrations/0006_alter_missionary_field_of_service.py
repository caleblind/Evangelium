# Generated by Django 4.2.16 on 2024-10-25 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseApp', '0005_missionary_field_of_service_alter_church_pastor_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='missionary',
            name='field_of_service',
            field=models.CharField(max_length=100),
        ),
    ]
