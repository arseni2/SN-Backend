# Generated by Django 3.2.2 on 2021-06-29 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0007_alter_postwall_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postwall',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='post'),
        ),
    ]
