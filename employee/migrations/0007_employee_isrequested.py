# Generated by Django 4.2.4 on 2023-10-12 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0006_employee_isverified'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='isRequested',
            field=models.BooleanField(default=False),
        ),
    ]