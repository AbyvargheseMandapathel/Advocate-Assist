# Generated by Django 4.2.4 on 2023-08-30 11:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_customuser_state'),
    ]

    operations = [
        migrations.CreateModel(
            name='LawyerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specialization', models.CharField(choices=[('family', 'Family Lawyer'), ('criminal', 'Criminal Lawyer'), ('consumer', 'Consumer Lawyer')], max_length=20)),
                ('start_date', models.DateField()),
                ('experience', models.IntegerField()),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='lawyer_profiles/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='lawyer_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
