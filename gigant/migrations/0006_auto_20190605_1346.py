# Generated by Django 2.2.1 on 2019-06-05 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gigant', '0005_auto_20190604_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=3, max_digits=9),
        ),
    ]
