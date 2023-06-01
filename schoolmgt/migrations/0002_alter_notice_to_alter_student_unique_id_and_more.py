# Generated by Django 4.1.5 on 2023-06-01 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolmgt', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='to',
            field=models.CharField(choices=[('teacher', 'teacher'), ('student', 'student'), ('admin', 'admin'), ('parent', 'parent')], max_length=50),
        ),
        migrations.AlterField(
            model_name='student',
            name='unique_id',
            field=models.CharField(default='34BB0', editable=False, max_length=10),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='unique_id',
            field=models.CharField(default='27805', editable=False, max_length=10),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('teacher', 'teacher'), ('student', 'student'), ('admin', 'admin'), ('parent', 'parent')], max_length=50),
        ),
    ]