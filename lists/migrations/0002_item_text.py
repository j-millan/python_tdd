# Generated by Django 3.1.1 on 2020-09-23 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='text',
            field=models.CharField(default='', max_length=150),
        ),
    ]