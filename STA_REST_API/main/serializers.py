from rest_framework import serializers
# from django.contrib.auth.models import User
from .models import TestGroupModel, TestResultModel


class TestGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestGroupModel
        fields = [
            'name',
            'file',
            'user'
        ]

class TestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResultModel
        fields = [
            'website_url',
            'user',
            'test_group',
            'run_time',
            'errors',
            'webpage_size',
            'run_date'
        ]