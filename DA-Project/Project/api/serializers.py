from rest_framework import serializers
from order.models import Order, OrderItem
from account.models import User
from shop.models import Product, Version, Series, Variation, ReviewRating
from category.models import *
from news.models import News


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class SeriesSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer()
    class Meta:
        model = Series
        fields = "__all__"


class VersionSerializer(serializers.ModelSerializer):
    series = SeriesSerializer()
    category = CategoriesSerializer()
    class Meta:
        model = Version
        fields = "__all__"


class VariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variation
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    variation = VariationSerializer(many=True, source="variation_set", required=False)
    class Meta:
        model = Product
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'phone', 'address', 'last_login', 'is_active', 'is_staff']
        extra_kwargs = {'email': {'validators': []},}

    def to_representation(self, data):
        data = super(UserSerializer, self).to_representation(data)
        data['full_name'] = '' if data['full_name']==None else data['full_name']
        data['phone'] = '' if data['phone']==None else data['phone']
        data['address'] = '' if data['address']==None else data['address']
        return data


class OrderItemSerializer(serializers.ModelSerializer):
    product_name= serializers.ReadOnlyField(source='product.version.name')
    capacity= serializers.ReadOnlyField(source='product.capacity')
    class Meta:
        model = OrderItem
        fields = ['id', 'color', 'quantity', 'price', 'product', 'product_name', 'capacity' ]

class OrderSerializer(serializers.ModelSerializer):
    orderitem = OrderItemSerializer(many=True, source='orderitem_set', required=False)
    customer = UserSerializer(required=False)

    class Meta:
        model = Order
        fields = '__all__'

    def update(self, instance, validated_data):

        instance.id = validated_data.get('username', instance.id)
        instance.transaction_id = validated_data.get('email', instance.transaction_id)
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.address = validated_data.get('address', instance.address)
        instance.state = validated_data.get('state', instance.state)
        instance.city = validated_data.get('city', instance.city)
        instance.note = validated_data.get('note', instance.note)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewRating
        fields = '__all__'


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'