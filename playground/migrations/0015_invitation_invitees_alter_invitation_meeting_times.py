# Generated by Django 4.2.3 on 2023-07-27 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0014_invitation_remove_validation_person_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='invitees',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='meeting_times',
            field=models.TextField(null=True),
        ),
    ]