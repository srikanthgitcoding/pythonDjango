# Generated by Django 4.1.3 on 2022-11-22 13:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_cartitem_cart'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cartitem',
            unique_together={('cart', 'product')},
        ),
    ]
