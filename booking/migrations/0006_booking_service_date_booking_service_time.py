# Generated by Django 4.2.4 on 2023-10-23 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0005_alter_booking_booking_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='service_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='service_time',
            field=models.TimeField(null=True),
        ),
    ]