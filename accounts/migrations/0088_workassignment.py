# Generated by Django 4.2.4 on 2023-09-30 16:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0087_student_lawyer'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('deadline_date', models.DateField()),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.case')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.student')),
            ],
        ),
    ]
