# Generated by Django 2.2.1 on 2019-06-04 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gigant', '0004_product_car'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
