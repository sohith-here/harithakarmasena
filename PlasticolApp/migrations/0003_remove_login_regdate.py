# Generated by Django 5.0 on 2023-12-06 04:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PlasticolApp', '0002_civilians'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='login',
            name='regDate',
        ),
    ]
