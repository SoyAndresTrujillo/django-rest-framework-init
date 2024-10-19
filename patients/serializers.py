from datetime import datetime
from rest_framework import serializers
from .models import Patient, Insurance, MedicalRecord


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"

    def validate_email(self, value):
        if "@example.com" in value:
            return value
        raise serializers.ValidationError("Email should contain @example.com")

    def validate(self, attrs):
        if len(attrs["contact_number"]) < 10:
            raise serializers.ValidationError(
                "Contact number must be at least 10 digits"
            )

        if not attrs["medical_history"] or len(attrs["medical_history"]) < 20:
            raise serializers.ValidationError(
                "Medical history must be at least 20 characters"
            )

        if attrs["date_of_birth"] > datetime.now().date():
            raise serializers.ValidationError("Date of birth cannot be in the future")

        return super().validate(attrs)


class InsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insurance
        fields = "__all__"


class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = "__all__"
