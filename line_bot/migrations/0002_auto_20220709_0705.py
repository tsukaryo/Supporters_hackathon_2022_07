# Generated by Django 3.1 on 2022-07-09 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('line_bot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]