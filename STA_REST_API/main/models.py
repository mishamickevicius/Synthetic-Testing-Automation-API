from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.contrib.postgres.fields import ArrayField


# Create your models here.

class Tester(User):
    """An model that extends the Django user model"""
    user_id = models.CharField(max_length=75) # This will be the user ID from givin from firebase
    class Meta:
        proxy = True

class TestGroupModel(models.Model):
    """
    This model will hold the .txt or .csv file that a user inputs
    """
    name = models.CharField(max_length=25) # Name of the TestGroup # * Needs to be unique for the user
    file = models.FileField(validators=[
        FileExtensionValidator(['txt', 'csv']), ]) # Only accepts txt and csv files
    user = models.ForeignKey('Tester', on_delete=models.CASCADE) # Link the user that owns this Test Group

class TestResultModel(models.Model):
    """
    This is a model that will store data from ran tests.
    Each Row will be a test
    """
    website_name = models.CharField(max_length=250)  # The name of the website being tested.
    user = models.ForeignKey('Tester', on_delete=models.CASCADE) # Link the user that owns this Test Group
    test_group = models.ForeignKey('TestGroupModel', on_delete=models.SET_NULL, null=True) # Link to the test group
    run_time = models.FloatField() # The run time of the website in seconds
    screenshot = models.ImageField() # ! Need to Fix
    errors = ArrayField(
        base_field=models.TextField(max_length=200, null=True)
    )
    webpage_size = models.FloatField() # The size of the webpage data in Mb

