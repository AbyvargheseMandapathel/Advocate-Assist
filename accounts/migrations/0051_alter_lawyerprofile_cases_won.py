# Generated by Django 4.2.4 on 2023-09-12 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0050_alter_lawyerprofile_cases_lost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lawyerprofile',
            name='cases_won',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
