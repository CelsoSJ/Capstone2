# Generated by Django 5.1.3 on 2024-11-30 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dean', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='middle_initial',
            field=models.CharField(blank=True, max_length=1, null='True'),
        ),
    ]