# Generated by Django 4.2.5 on 2023-11-19 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='workerreport',
            name='report_pdf',
            field=models.FileField(blank=True, null=True, upload_to='worker_reports/'),
        ),
    ]
