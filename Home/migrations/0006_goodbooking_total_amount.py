# Generated by Django 3.2.14 on 2023-04-22 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0005_goodbooking_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='goodbooking',
            name='total_amount',
            field=models.FloatField(null=True),
        ),
    ]
