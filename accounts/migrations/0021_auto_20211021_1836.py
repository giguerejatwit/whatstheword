# Generated by Django 3.2.4 on 2021-10-21 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_auto_20211008_0947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='instagramID',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='linkedinID',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='snapchatID',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
