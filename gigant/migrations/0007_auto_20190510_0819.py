# Generated by Django 2.1.7 on 2019-05-10 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gigant', '0006_auto_20190510_0802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='items',
            field=models.ManyToManyField(blank=True, to='gigant.CartItem'),
        ),
    ]
