# Generated by Django 3.0.9 on 2020-08-10 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lcore', '0005_remove_article_image_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='extract',
            field=models.CharField(max_length=300),
        ),
    ]
