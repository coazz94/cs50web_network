# Generated by Django 4.1.1 on 2022-10-22 19:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_followers'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Followers',
            new_name='Follower',
        ),
    ]