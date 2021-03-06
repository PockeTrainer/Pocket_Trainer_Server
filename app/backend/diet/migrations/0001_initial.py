# Generated by Django 3.2.8 on 2022-03-10 18:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DayHistoryDiet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateField()),
                ('time', models.CharField(blank=True, max_length=200, null=True)),
                ('food_name', models.CharField(blank=True, max_length=200, null=True)),
                ('food_g', models.IntegerField(blank=True, null=True)),
                ('food_kcal', models.IntegerField(blank=True, null=True)),
                ('carbohydrate', models.FloatField(blank=True, null=True)),
                ('protein', models.FloatField(blank=True, null=True)),
                ('province', models.FloatField(blank=True, null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='day_history_diet_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
