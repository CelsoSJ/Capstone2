# Generated by Django 5.1.3 on 2024-12-01 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faculty', '0003_remove_document_file_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='document_type',
            field=models.CharField(max_length=100),
        ),
    ]
