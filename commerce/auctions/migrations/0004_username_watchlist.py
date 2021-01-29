# Generated by Django 3.1.3 on 2021-01-28 19:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_product_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='username',
            name='watchlist',
            field=models.ForeignKey(default=False, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='auctions.product'),
        ),
    ]