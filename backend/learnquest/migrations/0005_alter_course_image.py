# Generated by Django 4.2.2 on 2023-07-09 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learnquest', '0004_alter_review_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(blank=True, default='default_course.jpg', null=True, upload_to='courses/'),
        ),
    ]
