# Generated by Django 4.1.1 on 2022-09-29 06:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cakestore', '0015_alter_cart_created_alter_cart_item'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='cart',
            new_name='cart_id',
        ),
    ]
