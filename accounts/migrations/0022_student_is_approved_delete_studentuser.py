# Generated by Django 4.2.4 on 2023-09-03 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_studentuser_alter_lawyerprofile_specialization'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='StudentUser',
        ),
    ]
