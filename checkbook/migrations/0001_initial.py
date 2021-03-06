# Generated by Django 2.0.5 on 2018-05-31 02:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text=' .category name', max_length=100)),
                ('frequency', models.CharField(blank=True, help_text=' .M(monthly) or W(weekly)', max_length=10, null=True)),
                ('budget', models.IntegerField(default=0, help_text=' .budgeted amount by frequency')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Check',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dater', models.DateField(help_text=' .the date of the transaction')),
                ('type', models.CharField(choices=[('CR', 'credit'), ('DR', 'debit')], help_text=' .credit or debit', max_length=2)),
                ('name', models.CharField(help_text=' .description', max_length=100)),
                ('amount', models.IntegerField(default=0, help_text=' .amount')),
                ('cleared', models.BooleanField(default=False, help_text=' .cleared with the bank?')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='checkbook.Category')),
            ],
            options={
                'ordering': ['dater'],
            },
        ),
    ]
