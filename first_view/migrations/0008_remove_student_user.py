# Generated by Django 5.1.3 on 2025-01-23 00:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first_view', '0007_alter_student_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='user',
        ),
    ]
