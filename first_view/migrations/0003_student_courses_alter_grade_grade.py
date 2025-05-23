# Generated by Django 5.1.3 on 2025-01-21 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_view', '0002_alter_lesson_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='courses',
            field=models.ManyToManyField(to='first_view.lesson'),
        ),
        migrations.AlterField(
            model_name='grade',
            name='grade',
            field=models.FloatField(choices=[(1.0, 1.0), (1.5, 1.5), (2.0, 2.0), (2.5, 2.5), (3.0, 3.0), (3.5, 3.5), (4.0, 4.0), (4.5, 4.5), (5.0, 5.0), (5.5, 5.5), (6.0, 6.0)]),
        ),
    ]
