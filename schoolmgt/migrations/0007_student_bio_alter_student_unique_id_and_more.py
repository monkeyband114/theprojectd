# Generated by Django 4.1.5 on 2023-05-29 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolmgt', '0006_student_unique_id_alter_student_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='unique_id',
            field=models.CharField(default='DD8AD', editable=False, max_length=10),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='unique_id',
            field=models.CharField(default='97C16', editable=False, max_length=10),
        ),
    ]
