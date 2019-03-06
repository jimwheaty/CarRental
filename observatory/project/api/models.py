# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Admin(models.Model):
    password = models.CharField(db_column='Password', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Admin'


class Amenities(models.Model):
    observation = models.ForeignKey('Observation', models.DO_NOTHING, db_column='Observation_id')  # Field name made lowercase.
    amenity = models.CharField(db_column='Amenity', max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Amenities'
        unique_together = (('observation', 'amenity'),)


class AmenitiesOffer(models.Model):
    amenity = models.CharField(db_column='Amenity', max_length=50)  # Field name made lowercase.
    offer = models.ForeignKey('Offer', models.DO_NOTHING, db_column='Offer_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Amenities_offer'
        unique_together = (('amenity', 'offer'),)


class App(models.Model):
    avatar = models.CharField(db_column='Avatar', max_length=255)  # Field name made lowercase.
    rating = models.FloatField(db_column='Rating', blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'App'


class Avatar(models.Model):
    avatar_id = models.BigAutoField(db_column='Avatar_id', primary_key=True)  # Field name made lowercase.
    avatar_path = models.CharField(db_column='Avatar_path', unique=True, max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Avatar'


class ClickCompany(models.Model):
    company = models.ForeignKey('Company', models.DO_NOTHING, db_column='Company_id')  # Field name made lowercase.
    click_date = models.DateTimeField(db_column='Click_date')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Click_company'


class ClickObservation(models.Model):
    observation = models.ForeignKey('Observation', models.DO_NOTHING, db_column='Observation_id')  # Field name made lowercase.
    click_date = models.DateTimeField(db_column='Click_date')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Click_observation'


class ClickOffer(models.Model):
    offer = models.ForeignKey('Offer', models.DO_NOTHING, db_column='Offer_id')  # Field name made lowercase.
    click_date = models.DateTimeField(db_column='Click_date')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Click_offer'


class CommentApp(models.Model):
    comment_id = models.BigAutoField(db_column='Comment_id', primary_key=True)  # Field name made lowercase.
    volunteer = models.ForeignKey('Volunteer', models.DO_NOTHING, db_column='Volunteer_id')  # Field name made lowercase.
    comment = models.CharField(db_column='Comment', max_length=255)  # Field name made lowercase.
    count_likes = models.IntegerField(db_column='Count_likes')  # Field name made lowercase.
    date = models.DateTimeField(db_column='Date')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Comment_app'


class CommentObservation(models.Model):
    comment_id = models.BigAutoField(db_column='Comment_id', primary_key=True)  # Field name made lowercase.
    observation = models.ForeignKey('Observation', models.DO_NOTHING, db_column='Observation_id')  # Field name made lowercase.
    volunteer = models.ForeignKey('Volunteer', models.DO_NOTHING, db_column='Volunteer_id')  # Field name made lowercase.
    comment = models.CharField(db_column='Comment', max_length=150)  # Field name made lowercase.
    count_likes = models.IntegerField(db_column='Count_likes')  # Field name made lowercase.
    date = models.DateTimeField(db_column='Date')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Comment_observation'


class Company(models.Model):
    company_id = models.BigAutoField(db_column='Company_id', primary_key=True)  # Field name made lowercase.
    token = models.CharField(db_column='Token', max_length=10, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', unique=True, max_length=50)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=255, blank=True, null=True)  # Field name made lowercase.
    rewarding = models.IntegerField(db_column='Rewarding', blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=100, blank=True, null=True)  # Field name made lowercase.
    lng = models.FloatField(db_column='Lng')  # Field name made lowercase.
    lat = models.FloatField(db_column='Lat')  # Field name made lowercase.
    withdrawn = models.CharField(db_column='Withdrawn', max_length=20, blank=True, null=True)  # Field name made lowercase.
    site_link = models.CharField(db_column='Site_link', unique=True, max_length=255, blank=True, null=True)  # Field name made lowercase.
    ranking = models.IntegerField(db_column='Ranking', blank=True, null=True)  # Field name made lowercase.
    avatar_id = models.BigIntegerField(db_column='Avatar_id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Company'


class Email(models.Model):
    email = models.CharField(db_column='Email', unique=True, max_length=50)  # Field name made lowercase.
    company = models.ForeignKey(Company, models.DO_NOTHING, db_column='Company_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Email'


class Observation(models.Model):
    observation_id = models.BigAutoField(db_column='Observation_id', primary_key=True)  # Field name made lowercase.
    volunteer = models.ForeignKey('Volunteer', models.DO_NOTHING, db_column='Volunteer_id', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    withdrawn = models.CharField(db_column='Withdrawn', max_length=13, blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=255, blank=True, null=True)  # Field name made lowercase.
    company_name = models.CharField(db_column='Company_name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ranking = models.IntegerField(db_column='Ranking', blank=True, null=True)  # Field name made lowercase.
    cheer_count = models.IntegerField(db_column='Cheer_count', blank=True, null=True)  # Field name made lowercase.
    x = models.FloatField(db_column='X', blank=True, null=True)  # Field name made lowercase.
    y = models.FloatField(db_column='Y', blank=True, null=True)  # Field name made lowercase.
    validation = models.CharField(db_column='Validation', max_length=6, blank=True, null=True)  # Field name made lowercase.
    company = models.ForeignKey(Company, models.DO_NOTHING, db_column='Company_id', blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=20)  # Field name made lowercase.
    stars = models.IntegerField(db_column='Stars', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Observation'


class Offer(models.Model):
    offer_id = models.BigAutoField(db_column='Offer_id', primary_key=True)  # Field name made lowercase.
    company = models.ForeignKey(Company, models.DO_NOTHING, db_column='Company_id')  # Field name made lowercase.
    price = models.FloatField(db_column='Price')  # Field name made lowercase.
    brand = models.CharField(db_column='Brand', max_length=30)  # Field name made lowercase.
    model = models.CharField(db_column='Model', max_length=50)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=50)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=50)  # Field name made lowercase.
    date = models.DateTimeField(db_column='Date')  # Field name made lowercase.
    stars = models.IntegerField(db_column='Stars')  # Field name made lowercase.
    cheer_count = models.IntegerField(db_column='Cheer_count')  # Field name made lowercase.
    x = models.FloatField(db_column='X')  # Field name made lowercase.
    y = models.FloatField(db_column='Y')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Offer'


class Photo(models.Model):
    observation = models.ForeignKey(Observation, models.DO_NOTHING, db_column='Observation_id')  # Field name made lowercase.
    path = models.CharField(db_column='Path', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Photo'
        unique_together = (('observation', 'path'),)


class Price(models.Model):
    price_id = models.BigAutoField(db_column='Price_id', primary_key=True)  # Field name made lowercase.
    price = models.FloatField(db_column='Price')  # Field name made lowercase.
    date = models.CharField(db_column='Date', max_length=10)  # Field name made lowercase.
    observation = models.ForeignKey(Observation, models.DO_NOTHING, db_column='Observation_id')  # Field name made lowercase.
    company = models.ForeignKey(Company, models.DO_NOTHING, db_column='Company_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Price'


class TelephoneNumber(models.Model):
    number = models.IntegerField(db_column='Number', unique=True)  # Field name made lowercase.
    company = models.ForeignKey(Company, models.DO_NOTHING, db_column='Company_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Telephone_number'


class Volunteer(models.Model):
    volunteer_id = models.BigAutoField(db_column='Volunteer_id', primary_key=True)  # Field name made lowercase.
    token = models.CharField(db_column='Token', max_length=10, blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='Username', max_length=50)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=255)  # Field name made lowercase.
    firstname = models.CharField(db_column='FirstName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    lastname = models.CharField(db_column='LastName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ranking = models.IntegerField(db_column='Ranking')  # Field name made lowercase.
    avatar = models.ForeignKey(Avatar, models.DO_NOTHING, db_column='Avatar_id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Volunteer'
        unique_together = (('volunteer_id', 'username'), ('volunteer_id', 'email'), ('volunteer_id', 'email'),)
