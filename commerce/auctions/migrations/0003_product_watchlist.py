# Generated by Django 3.1.3 on 2021-01-28 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20210126_1508'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='watchlist',
            field=models.BooleanField(default=False),
        ),
    ]
