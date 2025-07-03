from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Patient, MedicalRecord

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=Profile.ROLE_CHOICES, write_only=True)
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
    def validate_username(self, value):
        if User.objects.filter(username__exact=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value
    # For output
    profile_role = serializers.SerializerMethodField()

    def create(self, validated_data):
        role = validated_data.pop('role')
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
        )
        Profile.objects.create(user=user, role=role)
        return user

    def get_profile_role(self, obj):
        return obj.profile.role


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class PatientSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ('created_by',)

    def get_created_by(self, obj):
        # return f"{obj.created_by.first_name} {obj.created_by.last_name}".strip()
        return Patient.objects.get(pk=obj.pk).created_by.username

class MedicalRecordSerializer(serializers.ModelSerializer):
    patient = serializers.SerializerMethodField()
    class Meta:
        model = MedicalRecord
        fields = '__all__'
        read_only_fields = ('created_at',)

    def get_patient(self, obj):
            return f"{obj.patient.name}"