# Generated by Django 3.2.10 on 2021-12-17 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simplewf', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simpleworkflow',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
