# Generated by Django 3.2.4 on 2025-04-29 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0004_alter_stockmovement_quantite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockmovement',
            name='quantite',
            field=models.IntegerField(),
        ),
    ]
