# Generated by Django 3.2.2 on 2021-05-28 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0004_alter_postwall_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postwall',
            name='like',
            field=models.ManyToManyField(blank=True, to='Profile.LikePost'),
        ),
    ]
