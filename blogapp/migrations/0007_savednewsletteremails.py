# Generated by Django 3.1.7 on 2021-09-04 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0006_myuser_about_writer'),
    ]

    operations = [
        migrations.CreateModel(
            name='SavedNewsletterEmails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]
