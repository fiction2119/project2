# Generated by Django 3.1.3 on 2021-01-21 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0018_auto_20210121_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='initial_bid',
            field=models.IntegerField(),
        ),
    ]