# Generated by Django 3.1.7 on 2021-09-02 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0006_blogpost_is_popular'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='image',
            field=models.ImageField(null=True, upload_to='userimage/%m/%d/'),
        ),
    ]