# Generated by Django 5.0.1 on 2024-04-05 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0020_expense_expensehistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='expense',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='expense',
            name='income',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
