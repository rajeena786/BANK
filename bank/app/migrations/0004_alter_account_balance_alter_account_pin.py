# Generated by Django 5.1.5 on 2025-02-06 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_account_pin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='balance',
            field=models.PositiveBigIntegerField(default=500),
        ),
        migrations.AlterField(
            model_name='account',
            name='pin',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
