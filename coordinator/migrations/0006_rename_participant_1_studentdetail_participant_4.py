# Generated by Django 5.0.6 on 2024-11-10 04:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coordinator', '0005_rename_cont_num_studentdetail_contact_number_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentdetail',
            old_name='participant_1',
            new_name='participant_4',
        ),
    ]
