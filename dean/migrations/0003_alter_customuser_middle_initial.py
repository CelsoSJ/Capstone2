# Generated by Django 5.1.3 on 2024-11-30 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dean', '0002_alter_customuser_middle_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='middle_initial',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
    ]
