# Generated by Django 5.0.1 on 2024-02-03 06:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_app', '0004_contact_alter_news_published_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='published_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 3, 6, 27, 19, 761687, tzinfo=datetime.timezone.utc)),
        ),
    ]