# Generated by Django 3.0.7 on 2021-02-06 22:12

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RideDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(max_length=200)),
                ('driver', models.CharField(blank=True, max_length=200, null=True)),
                ('sharable', models.BooleanField(default=True)),
                ('remaining_seats', models.IntegerField(default=0)),
                ('status', models.CharField(default='Open', max_length=20)),
                ('destination', models.CharField(blank=True, max_length=200, null=True)),
                ('arrival_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('vehicle', models.CharField(default='Sedan', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=200)),
                ('vehicle', models.CharField(default='Sedan', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_role', models.CharField(max_length=20)),
                ('party_size', models.IntegerField(default=1)),
                ('ride_detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ride.RideDetail')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ride.User')),
            ],
        ),
    ]
