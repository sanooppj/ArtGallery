# Generated by Django 5.0.3 on 2024-04-03 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("BackEnd", "0010_appliedcoupon_discounted_amount_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="coupondb",
            name="status",
            field=models.BooleanField(default=True),
        ),
    ]
