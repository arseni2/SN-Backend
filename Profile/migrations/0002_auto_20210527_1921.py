# Generated by Django 3.2.2 on 2021-05-27 19:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='likepost',
            old_name='likeLike',
            new_name='likes',
        ),
        migrations.RenameField(
            model_name='likepost',
            old_name='userLike',
            new_name='user',
        ),
    ]
