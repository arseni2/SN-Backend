# Generated by Django 3.2.2 on 2021-05-28 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0006_alter_likepost_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postwall',
            name='like',
            field=models.ManyToManyField(blank=True, default=1, to='Profile.LikePost'),
        ),
    ]