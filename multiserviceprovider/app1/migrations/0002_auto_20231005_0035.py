# Generated by Django 4.2.5 on 2023-10-04 19:05

from django.db import migrations,models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]
    operations = [
        migrations.AlterField(
            model_name='MyUser',
            name='email',
            field=models.EmailField(max_length=254, unique=True)  # Add unique constraint
        ),
    ]