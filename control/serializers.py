


from .models import Ticket
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Category
User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password']
        extra_kwargs = {
            'email': {'required': True},
            'phone': {'required': True}
        }

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data.get('phone', ''),
            password=validated_data['password']
        )
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'role', 'created_at']

        read_only_fields = ['id', 'role', 'created_at', 'username']




class CategorySerializer(serializers.ModelSerializer):

    name = serializers.CharField(
        max_length=50,
        validators=[UniqueValidator(
            queryset=Category.objects.all(),
            message="Bunday nomli kategoriya allaqachon mavjud."
        )]
    )

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']



class TicketSerializer(serializers.ModelSerializer):
    client = serializers.StringRelatedField(read_only=True)

    operator = serializers.SerializerMethodField()
    category_name = serializers.CharField(
        source="category.name",
        read_only=True
    )

    class Meta:
        model = Ticket
        fields = [
            "id",
            "title",
            "description",
            "client",
            "operator",
            "category",
            "category_name",
            "status",
            "priority",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "client",
            "operator",
            "category_name",
            "status",
            "created_at",
            "updated_at",
        ]

    def get_operator(self, obj):
        if not obj.operator:
            return None

        return {
            "id": obj.operator.id,
            "username": obj.operator.username,
        }