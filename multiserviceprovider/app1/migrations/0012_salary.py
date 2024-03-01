# Generated by Django 4.2.5 on 2024-02-29 04:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0011_faq'),
    ]

    operations = [
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('salaryid', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(default='pending', max_length=15)),
                ('branchid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.branch')),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]