# Generated by Django 5.1.2 on 2024-12-07 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0006_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
