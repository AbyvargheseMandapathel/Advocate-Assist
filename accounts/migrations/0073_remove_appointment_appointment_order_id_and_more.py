# Generated by Django 4.2.4 on 2023-09-19 14:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0072_appointment_appointment_order_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='appointment_order_id',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='payment_id',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='signature_id',
        ),
    ]
