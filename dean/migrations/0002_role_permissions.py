# Generated by Django 4.2 on 2024-10-19 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('dean', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='permissions',
            field=models.ManyToManyField(to='auth.permission'),
        ),
    ]
