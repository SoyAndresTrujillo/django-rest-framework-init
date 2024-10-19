from datetime import datetime
from rest_framework import serializers

from bookings.serializers import AppointmentSerializer
from .models import Patient, Insurance, MedicalRecord


class PatientSerializer(serializers.ModelSerializer):
    # Create a new appointment for a patient
    #     python ./manage.py shell
    # >>> from datetime import date, time
    # >>> from doctors.models import Doctor
    # >>> from patients.models import Patient
    # >>> from bookings.models import Appointment
    # >>> patient = Patient.objects.get(id=2)
    # >>> doctor = Doctor.objects.first()
    # >>> Appointment.objects.create(patient=patient, doctor=doctor, appointment_date=date(2022, 12, 5), appointment_time=time(9, 0), notes="Ejemplo", status="HECHA")
    appointments = AppointmentSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        # the order to read the fields is important, firts search the field in class,
        # then in the related model
        # if not found field, error is raised
        fields = [
            "id",
            "first_name",
            "last_name",
            "date_of_birth",
            "contact_number",
            "email",
            "address",
            "medical_history",
            "appointments",
        ]

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
