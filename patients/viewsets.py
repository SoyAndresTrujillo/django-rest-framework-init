from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import PatientSerializer, InsuranceSerializer, MedicalRecordSerializer
from .models import Patient, Insurance, MedicalRecord


class ListPatientView(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()

    @action(["GET"], detail=True, url_path="get-medical-history")
    def get_medical_history(self, request, pk):
        patient = self.get_object()
        return Response({"medical_history": patient.medical_history})


class ListInsuranceView(viewsets.ModelViewSet):
    serializer_class = InsuranceSerializer
    queryset = Insurance.objects.all()


class ListMedicalRecordView(viewsets.ModelViewSet):
    serializer_class = MedicalRecordSerializer
    queryset = MedicalRecord.objects.all()
