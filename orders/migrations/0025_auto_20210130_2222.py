# Generated by Django 2.1.5 on 2021-01-31 03:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0024_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='cart_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='orders.Cart'),
        ),
    ]
