# Generated by Django 5.1.2 on 2024-10-22 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("weather", "0002_countryweather_date_countryweather_dew_point_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="countryweather",
            name="date",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="countryweather",
            name="time",
            field=models.CharField(max_length=100, null=True),
        ),
    ]
