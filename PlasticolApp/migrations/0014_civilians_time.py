# Generated by Django 4.2.10 on 2024-03-07 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PlasticolApp', '0013_rename_members_civilians_ward'),
    ]

    operations = [
        migrations.AddField(
            model_name='civilians',
            name='time',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
