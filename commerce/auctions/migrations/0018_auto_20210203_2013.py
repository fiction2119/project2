# Generated by Django 3.1.3 on 2021-02-03 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(default=None, max_length=56),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
