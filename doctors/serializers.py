from rest_framework import serializers

from .models import Department, Doctor, DoctorAvailability, MedicalNote
from bookings.serializers import AppointmentSerializer


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class DoctorSerializer(serializers.ModelSerializer):
    appointments = AppointmentSerializer(many=True, read_only=True)

    class Meta:
        model = Doctor
        fields = [
            "id",
            "first_name",
            "last_name",
            "qualification",
            "contact_number",
            "email",
            "address",
            "biography",
            "is_on_vacation",
            "appointments",
        ]

    # Custom validation for email
    def validate_email(self, value):
        if "@example.com" in value:
            return value
        raise serializers.ValidationError("Email should contain @example.com")

    def validate(self, attrs):
        if len(attrs["contact_number"]) < 10 and attrs["is_on_vacation"]:
            raise serializers.ValidationError(
                "Contact number must be at least 10 digits"
            )
        return super().validate(attrs)


class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorAvailability
        fields = "__all__"


class MedicalNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalNote
        fields = "__all__"
