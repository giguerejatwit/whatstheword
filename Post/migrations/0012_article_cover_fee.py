# Generated by Django 3.2.4 on 2021-09-07 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0011_auto_20210904_1834'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='cover_fee',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
