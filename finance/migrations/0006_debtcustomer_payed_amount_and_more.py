# Generated by Django 4.2.7 on 2023-11-17 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0005_deptarrivedcargo_payed_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='debtcustomer',
            name='payed_amount',
            field=models.PositiveBigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='deptarrivedcargo',
            name='payed_amount',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]
