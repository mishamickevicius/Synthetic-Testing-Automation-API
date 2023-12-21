from django.contrib import admin
from .models import TestResultModel, TestGroupModel

# Register your models here.

class TestResultAdmin(admin.ModelAdmin):
    list_display = ['website_url', 'user', 'run_time']

admin.site.register(TestResultModel, TestResultAdmin)

class TestGroupAdmin(admin.ModelAdmin):
    list_display = ['name','user']

admin.site.register(TestGroupModel, TestGroupAdmin)