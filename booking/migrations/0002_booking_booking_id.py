# Generated by Django 4.2.4 on 2023-10-18 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='booking_id',
            field=models.CharField(max_length=70, null=True),
        ),
    ]