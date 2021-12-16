# Generated by Django 2.2.24 on 2021-11-29 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("socialprofile", "0012_auto_20211129_1613"),
    ]

    operations = [
        migrations.AlterField(
            model_name="socialprofile",
            name="gender",
            field=models.CharField(
                blank=True,
                choices=[
                    ("male", "Male"),
                    ("female", "Female"),
                    ("unknown", "Unknown"),
                ],
                default="unknown",
                max_length=10,
                null=True,
                verbose_name="Gender",
            ),
        ),
    ]
