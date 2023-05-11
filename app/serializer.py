from rest_framework import serializers
from .models import Tours, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tours
        fields = ['name', 'description', 'price', 'exist', 'category']