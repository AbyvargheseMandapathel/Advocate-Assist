# Generated by Django 4.2.4 on 2023-09-13 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0051_alter_lawyerprofile_cases_won'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lawyerprofile',
            name='budget',
        ),
        migrations.RemoveField(
            model_name='lawyerprofile',
            name='working_days',
        ),
        migrations.RemoveField(
            model_name='lawyerprofile',
            name='working_time_end',
        ),
        migrations.RemoveField(
            model_name='lawyerprofile',
            name='working_time_start',
        ),
        migrations.AddField(
            model_name='lawyerprofile',
            name='court',
            field=models.CharField(blank=True, choices=[('jfcmcchangancherry', 'Judicial First Class Magistrate Court  Changancherry'), ('criminal', 'Munsiff Court Changancherry'), ('jfcmcKanjirapally', 'Judicial First Class Magistrate Court  Kanjirapally'), ('munsifcourtkanjirapally', 'Munsiff Court Kanjirapally'), ('districtcourtkottayam', 'District Court Kottayam'), ('High Court Kochi', 'High Court Kochi')], max_length=200),
        ),
        migrations.AddField(
            model_name='lawyerprofile',
            name='currendly_handling',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lawyerprofile',
            name='total_cases_handeled',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='lawyerprofile',
            name='experience',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='lawyerprofile',
            name='specialization',
            field=models.CharField(blank=True, choices=[('family', 'Family Lawyer'), ('criminal', 'Criminal Lawyer'), ('consumer', 'Consumer Lawyer'), ('coperatelawyer', 'Coperate Lawyer'), ('civilrightlawyer', 'Civil Right Lawyer'), ('divorcelawyer', 'Divorce Lawyer')], max_length=20),
        ),
    ]
