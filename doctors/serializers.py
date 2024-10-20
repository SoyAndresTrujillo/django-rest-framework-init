from rest_framework import serializers
from datetime import datetime

from .models import Department, Doctor, DoctorAvailability, MedicalNote
from bookings.serializers import AppointmentSerializer


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorAvailability
        fields = "__all__"


class DoctorSerializer(serializers.ModelSerializer):
    appointments = AppointmentSerializer(many=True, read_only=True)
    # >>> from datetime import date, time
    # >>> from doctors.models import Doctor
    # >>> from .models import DoctorAvailability
    # >>> doctor = Doctor.objects.first()
    # >>> DoctorAvailability.objects.create(
    # ...     doctor=doctor,
    # ...     start_date=date(2022, 12, 5),
    # ...     end_date=date(2030, 12, 5),
    # ...     start_time=time(9, 0),
    # ...     end_time=time(17, 0)
    # ... )
    availabilities = DoctorAvailabilitySerializer(many=True, read_only=True)
    years_of_experience = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = [
            "id",
            "first_name",
            "last_name",
            "qualification",
            "years_of_experience",
            "contact_number",
            "email",
            "address",
            "biography",
            "is_on_vacation",
            "availabilities",
            "appointments",
        ]

    def get_years_of_experience(self, obj):
        first_availability = obj.availabilities.order_by("start_date").first()
        if first_availability:
            return (datetime.now().date() - first_availability.start_date).days // 365
        return 0

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


class MedicalNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalNote
        fields = "__all__"
