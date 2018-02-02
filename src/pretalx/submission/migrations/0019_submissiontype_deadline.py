# Generated by Django 2.0.1 on 2018-02-02 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0018_remove_submissiontype_max_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='submissiontype',
            name='deadline',
            field=models.DateTimeField(blank=True, help_text='If you want a different deadline than the global deadline for this submission type, enter it here.', null=True, verbose_name='deadline'),
        ),
    ]
