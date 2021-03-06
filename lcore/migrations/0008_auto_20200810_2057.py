# Generated by Django 3.0.9 on 2020-08-10 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lcore', '0007_category_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ManyToManyField(blank=True, to='lcore.Category'),
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(blank=True, to='lcore.Tag'),
        ),
    ]
