# Generated by Django 2.2.24 on 2021-11-29 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("socialprofile", "0014_auto_20211129_1729"),
    ]

    operations = [
        migrations.RenameField(
            model_name="socialprofile",
            old_name="google_plusUrl",
            new_name="google_url",
        ),
        migrations.AddField(
            model_name="socialprofile",
            name="facebook_url",
            field=models.URLField(
                blank=True, max_length=500, null=True, verbose_name="Facebook Profile"
            ),
        ),
        migrations.AddField(
            model_name="socialprofile",
            name="twitter_url",
            field=models.URLField(
                blank=True, max_length=500, null=True, verbose_name="Twitter Profile"
            ),
        ),
        migrations.AlterField(
            model_name="socialprofile",
            name="edited_by_provider",
            field=models.NullBooleanField(
                default=False, verbose_name="Social provider edited user's info"
            ),
        ),
    ]
