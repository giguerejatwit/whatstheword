# Generated by Django 3.2.4 on 2021-06-19 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='id', 
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False),
        ),
    ]
