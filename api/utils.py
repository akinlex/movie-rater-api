from . import models
from rest_framework import serializers

def max_min_validator(value):
    if value > 5:
        raise serializers.ValidationError('Rating cannot be more than 5.')
    elif value <= 0:
        raise serializers.ValidationError('Rating cannot be 0 or less than 0.')
    else:
        return value
