# Generated by Django 3.2.5 on 2021-07-02 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_alter_user_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.TextField(max_length=200, null=True),
        ),
    ]
