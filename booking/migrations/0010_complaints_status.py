# Generated by Django 4.2.4 on 2023-11-01 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0009_complaints'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaints',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('resolved', 'resolved'), ('solved', 'solved')], default='pending', max_length=50),
        ),
    ]
