from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from bookings.serializers import AppointmentSerializer
from bookings.models import Appointment

from .models import (
    Doctor,
    Department,
    DoctorAvailability,
    MedicalNote,
)
from .serializers import (
    DoctorSerializer,
    DepartmentSerializer,
    DoctorAvailabilitySerializer,
    MedicalNoteSerializer,
)
from .permissions import IsDoctor


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    @action(["POST"], detail=True, url_path="set-on-vacation")
    def set_on_vacation(self, request, pk):
        doctor = self.get_object()
        doctor.is_on_vacation = True
        doctor.save()
        return Response({"status": "Doctor is on vacation"})

    @action(["POST"], detail=True, url_path="set-off-vacation")
    def set_off_vacation(self, request, pk):
        doctor = self.get_object()
        doctor.is_on_vacation = False
        doctor.save()
        return Response({"status": "Doctor is not on vacation"})

    @action(
        ["GET", "POST", "DELETE"],
        url_path="appointments(?:/(?P<appointment_id>[^/.]+))?",
        detail=True,
        serializer_class=AppointmentSerializer,
    )
    def appointments(self, request, pk, appointment_id=None):
        doctor = self.get_object()
        data = request.data.copy()
        data["doctor"] = doctor.id

        if request.method == "POST":
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == "GET":
            appointments = Appointment.objects.filter(doctor=doctor.id)
            serializer = self.serializer_class(appointments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if request.method == "DELETE" and appointment_id:
            try:
                appointment = Appointment.objects.get(id=appointment_id)
                serializer = self.serializer_class(appointment)
                appointment.delete()
                return Response(status=status.HTTP_200_OK)

            except Appointment.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

    @action(
        ["DELETE", "GET"],
        detail=True,
        url_path="appointment/(?P<appointment_id>[^/.]+)",
        serializer_class=AppointmentSerializer,
    )
    def appointment(self, request, pk, appointment_id):
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            serializer = self.serializer_class(appointment)

            if request.method == "DELETE":
                appointment.delete()
                return Response(status=status.HTTP_200_OK)

            if request.method == "GET":
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Appointment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class DoctorAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = DoctorAvailability.objects.all()
    serializer_class = DoctorAvailabilitySerializer


class MedicalNoteViewSet(viewsets.ModelViewSet):
    queryset = MedicalNote.objects.all()
    serializer_class = MedicalNoteSerializer
