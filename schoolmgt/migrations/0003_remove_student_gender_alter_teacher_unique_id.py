# Generated by Django 4.1.5 on 2023-05-03 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolmgt', '0002_alter_teacher_unique_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='gender',
        ),
        migrations.AlterField(
            model_name='teacher',
            name='unique_id',
            field=models.CharField(default='B85F5', editable=False, max_length=10),
        ),
    ]
