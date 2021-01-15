# Generated by Django 3.1.3 on 2021-01-02 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='username',
            name='listings',
        ),
        migrations.AddField(
            model_name='username',
            name='product',
            field=models.ManyToManyField(blank=True, related_name='listing', to='auctions.Listing'),
        ),
    ]