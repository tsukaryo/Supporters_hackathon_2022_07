# Generated by Django 3.1 on 2022-07-10 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('line_bot', '0005_place_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='detail',
            field=models.CharField(default='NoCategory', max_length=200),
        ),
    ]
