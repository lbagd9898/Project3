# Generated by Django 2.1.5 on 2021-01-14 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pizzas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dough', models.CharField(max_length=12)),
                ('size', models.CharField(max_length=12)),
                ('toppings', models.CharField(max_length=15)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='Toppings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Toppings', models.CharField(max_length=7)),
            ],
        ),
    ]
