# Generated by Django 3.1.3 on 2021-02-03 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_auto_20210203_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='url',
            field=models.ImageField(blank=True, upload_to='products'),
        ),
    ]
