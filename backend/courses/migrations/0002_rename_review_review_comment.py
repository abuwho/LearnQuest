# Generated by Django 4.2.2 on 2023-06-29 14:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='review',
            new_name='comment',
        ),
    ]