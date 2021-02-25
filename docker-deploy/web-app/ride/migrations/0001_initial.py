# Generated by Django 3.1.5 on 2021-02-15 19:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RideDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(max_length=200)),
                ('owner_email', models.CharField(default='mosiqi1996@hotmail.com', max_length=200)),
                ('driver', models.CharField(blank=True, max_length=200, null=True)),
                ('sharable', models.BooleanField(default=True)),
                ('remaining_seats', models.IntegerField(default=0)),
                ('status', models.CharField(default='Open', max_length=20)),
                ('destination', models.CharField(blank=True, max_length=200, null=True)),
                ('arrival_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('vehicle', models.CharField(default='Sedan', max_length=20)),
                ('special_request', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_role', models.CharField(max_length=20)),
                ('party_size', models.IntegerField(default=1)),
                ('ride_detail', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ride.ridedetail')),
                ('user', models.ForeignKey(blank=True, db_column='user', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]