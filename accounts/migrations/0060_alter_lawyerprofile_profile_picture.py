# Generated by Django 4.2.4 on 2023-09-17 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0059_alter_lawyerprofile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lawyerprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='uploads/default_profile_picture.png', null=True, upload_to='uploads/'),
        ),
    ]
