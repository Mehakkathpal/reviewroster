# Generated by Django 4.1 on 2023-09-18 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stripepayment", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="AddSubscriptionStatus",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("customer_email", models.EmailField(max_length=254, unique=True)),
                ("subscribed_time", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
