from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.contrib.postgres.fields import ArrayField


# Create your models here.


class TestGroupModel(models.Model):
    """
    This model will hold the .txt or .csv file that a user inputs
    """
    name = models.CharField(max_length=25) # Name of the TestGroup # * Needs to be unique for the user
    # file = models.FileField(validators=[
    #     FileExtensionValidator(['txt', 'csv']), ]) # Only accepts txt and csv files
    file_data = ArrayField(
        base_field=models.TextField(max_length=200, null=True, blank=True)
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Link the user that owns this Test Group

    def __str__(self) -> str:
        return f"Name: {self.name}  User: {self.user}"
    

class TestResultModel(models.Model):
    """
    This is a model that will store data from ran tests.
    Each Row will be a test
    """
    website_url = models.CharField(max_length=250)  # The url of the website being tested.
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Link the user that owns this Test Group
    test_group = models.ForeignKey(TestGroupModel, on_delete=models.SET_NULL, null=True) # Link to the test group
    run_time = models.FloatField() # The run time of the website in seconds

    # ! Get Screenshots to work later
    # screenshot = models.FilePathField(path="/screenshots/", null=True) # Will be the file path to the image
    
    
    errors = ArrayField(
        base_field=models.TextField(max_length=200, null=True, blank=True)
    )
    webpage_size = models.FloatField(null=True, blank=True) # The size of the webpage data in Mb
    run_date = models.DateTimeField()

    def __str__(self) -> str:
        return f"URL: {self.website_url} User: {self.user}"