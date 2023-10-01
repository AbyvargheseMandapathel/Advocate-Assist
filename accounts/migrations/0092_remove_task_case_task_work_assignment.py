# Generated by Django 4.2.4 on 2023-10-01 17:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0091_alter_task_case'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='case',
        ),
        migrations.AddField(
            model_name='task',
            name='work_assignment',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.workassignment'),
            preserve_default=False,
        ),
    ]