# Generated by Django 3.2.4 on 2021-07-20 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0011_rename_author_id_article_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
