# Generated by Django 4.2.2 on 2023-07-14 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learnquest', '0006_lesson_summary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='price',
            field=models.FloatField(default=0.0, null=True),
        ),
    ]
