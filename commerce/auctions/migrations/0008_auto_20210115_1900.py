# Generated by Django 3.1.3 on 2021-01-15 19:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20210115_1828'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bid',
            old_name='bid',
            new_name='offer',
        ),
    ]
