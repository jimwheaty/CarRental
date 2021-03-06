# Generated by Django 2.1.7 on 2019-03-05 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(blank=True, db_column='Password', max_length=255, null=True)),
            ],
            options={
                'db_table': 'Admin',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Amenities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amenity', models.CharField(db_column='Amenity', max_length=100)),
            ],
            options={
                'db_table': 'Amenities',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AmenitiesOffer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amenity', models.CharField(db_column='Amenity', max_length=50)),
            ],
            options={
                'db_table': 'Amenities_offer',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.CharField(db_column='Avatar', max_length=255)),
                ('rating', models.FloatField(blank=True, db_column='Rating', null=True)),
                ('email', models.CharField(db_column='Email', max_length=50)),
            ],
            options={
                'db_table': 'App',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Avatar',
            fields=[
                ('avatar_id', models.BigAutoField(db_column='Avatar_id', primary_key=True, serialize=False)),
                ('avatar_path', models.CharField(db_column='Avatar_path', max_length=100, unique=True)),
            ],
            options={
                'db_table': 'Avatar',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ClickCompany',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('click_date', models.DateTimeField(db_column='Click_date')),
            ],
            options={
                'db_table': 'Click_company',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ClickObservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('click_date', models.DateTimeField(db_column='Click_date')),
            ],
            options={
                'db_table': 'Click_observation',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ClickOffer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('click_date', models.DateTimeField(db_column='Click_date')),
            ],
            options={
                'db_table': 'Click_offer',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CommentApp',
            fields=[
                ('comment_id', models.BigAutoField(db_column='Comment_id', primary_key=True, serialize=False)),
                ('comment', models.CharField(db_column='Comment', max_length=255)),
                ('count_likes', models.IntegerField(db_column='Count_likes')),
                ('date', models.DateTimeField(db_column='Date')),
            ],
            options={
                'db_table': 'Comment_app',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CommentObservation',
            fields=[
                ('comment_id', models.BigAutoField(db_column='Comment_id', primary_key=True, serialize=False)),
                ('comment', models.CharField(db_column='Comment', max_length=150)),
                ('count_likes', models.IntegerField(db_column='Count_likes')),
                ('date', models.DateTimeField(db_column='Date')),
            ],
            options={
                'db_table': 'Comment_observation',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('company_id', models.BigAutoField(db_column='Company_id', primary_key=True, serialize=False)),
                ('token', models.CharField(blank=True, db_column='Token', max_length=10, null=True)),
                ('name', models.CharField(db_column='Name', max_length=50, unique=True)),
                ('password', models.CharField(blank=True, db_column='Password', max_length=255, null=True)),
                ('rewarding', models.IntegerField(blank=True, db_column='Rewarding', null=True)),
                ('address', models.CharField(blank=True, db_column='Address', max_length=100, null=True)),
                ('lng', models.FloatField(db_column='Lng')),
                ('lat', models.FloatField(db_column='Lat')),
                ('withdrawn', models.CharField(blank=True, db_column='Withdrawn', max_length=20, null=True)),
                ('site_link', models.CharField(blank=True, db_column='Site_link', max_length=255, null=True, unique=True)),
                ('ranking', models.IntegerField(blank=True, db_column='Ranking', null=True)),
                ('avatar_id', models.BigIntegerField(blank=True, db_column='Avatar_id', null=True)),
            ],
            options={
                'db_table': 'Company',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(db_column='Email', max_length=50, unique=True)),
            ],
            options={
                'db_table': 'Email',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Observation',
            fields=[
                ('observation_id', models.BigAutoField(db_column='Observation_id', primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='Name', max_length=100)),
                ('withdrawn', models.CharField(blank=True, db_column='Withdrawn', max_length=13, null=True)),
                ('location', models.CharField(blank=True, db_column='Location', max_length=255, null=True)),
                ('company_name', models.CharField(blank=True, db_column='Company_name', max_length=50, null=True)),
                ('description', models.CharField(blank=True, db_column='Description', max_length=255, null=True)),
                ('ranking', models.IntegerField(blank=True, db_column='Ranking', null=True)),
                ('cheer_count', models.IntegerField(blank=True, db_column='Cheer_count', null=True)),
                ('x', models.FloatField(blank=True, db_column='X', null=True)),
                ('y', models.FloatField(blank=True, db_column='Y', null=True)),
                ('validation', models.CharField(blank=True, db_column='Validation', max_length=6, null=True)),
                ('category', models.CharField(db_column='Category', max_length=20)),
                ('stars', models.IntegerField(blank=True, db_column='Stars', null=True)),
            ],
            options={
                'db_table': 'Observation',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('offer_id', models.BigAutoField(db_column='Offer_id', primary_key=True, serialize=False)),
                ('price', models.FloatField(db_column='Price')),
                ('brand', models.CharField(db_column='Brand', max_length=30)),
                ('model', models.CharField(db_column='Model', max_length=50)),
                ('category', models.CharField(db_column='Category', max_length=50)),
                ('location', models.CharField(db_column='Location', max_length=50)),
                ('date', models.DateTimeField(db_column='Date')),
                ('stars', models.IntegerField(db_column='Stars')),
                ('cheer_count', models.IntegerField(db_column='Cheer_count')),
                ('x', models.FloatField(db_column='X')),
                ('y', models.FloatField(db_column='Y')),
            ],
            options={
                'db_table': 'Offer',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(db_column='Path', max_length=255)),
            ],
            options={
                'db_table': 'Photo',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('price_id', models.BigAutoField(db_column='Price_id', primary_key=True, serialize=False)),
                ('price', models.FloatField(db_column='Price')),
                ('date', models.CharField(db_column='Date', max_length=10)),
            ],
            options={
                'db_table': 'Price',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TelephoneNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(db_column='Number', unique=True)),
            ],
            options={
                'db_table': 'Telephone_number',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('volunteer_id', models.BigAutoField(db_column='Volunteer_id', primary_key=True, serialize=False)),
                ('token', models.CharField(blank=True, db_column='Token', max_length=10, null=True)),
                ('username', models.CharField(db_column='Username', max_length=50)),
                ('password', models.CharField(db_column='Password', max_length=255)),
                ('firstname', models.CharField(blank=True, db_column='FirstName', max_length=50, null=True)),
                ('lastname', models.CharField(blank=True, db_column='LastName', max_length=50, null=True)),
                ('email', models.CharField(blank=True, db_column='Email', max_length=50, null=True)),
                ('ranking', models.IntegerField(db_column='Ranking')),
            ],
            options={
                'db_table': 'Volunteer',
                'managed': False,
            },
        ),
    ]
