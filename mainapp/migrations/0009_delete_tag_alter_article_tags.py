# Generated by Django 4.2 on 2024-09-18 05:28

from django.db import migrations
import mainapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0008_remove_article_tags_article_tags'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Tag',
        ),
        migrations.AlterField(
            model_name='article',
            name='tags',
            field=mainapp.models.ListField(blank=True, null=True, token=','),
        ),
    ]
