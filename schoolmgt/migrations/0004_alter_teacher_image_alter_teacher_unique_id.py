# Generated by Django 4.1.5 on 2023-05-28 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolmgt', '0003_alter_teacher_unique_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='image',
            field=models.ImageField(default='testimon.png', null=True, upload_to='firststep/'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='unique_id',
            field=models.CharField(default='57D95', editable=False, max_length=10),
        ),
    ]