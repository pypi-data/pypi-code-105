# Generated by Django 2.2.25 on 2021-12-14 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialprofile', '0020_remove_socialprofile_last_accessed'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialprofile',
            name='facebook_avatar',
            field=models.URLField(blank=True, max_length=500, null=True, verbose_name='Facebook Avatar'),
        ),
        migrations.AddField(
            model_name='socialprofile',
            name='google_avatar',
            field=models.URLField(blank=True, max_length=500, null=True, verbose_name='Google Avatar'),
        ),
        migrations.AddField(
            model_name='socialprofile',
            name='instagram_avatar',
            field=models.URLField(blank=True, max_length=500, null=True, verbose_name='Instagram Avatar'),
        ),
        migrations.AddField(
            model_name='socialprofile',
            name='twitter_avatar',
            field=models.URLField(blank=True, max_length=500, null=True, verbose_name='Twitter Avatar'),
        ),
    ]
