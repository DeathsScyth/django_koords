# Generated by Django 4.2 on 2023-04-16 23:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='role',
        ),
    ]
