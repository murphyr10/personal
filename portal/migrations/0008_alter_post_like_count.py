# Generated by Django 5.1.7 on 2025-03-15 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0007_notification_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='like_count',
            field=models.BigIntegerField(default=0),
        ),
    ]
