from django.contrib.auth.models import User, Group
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from patients.models import Patient
from doctors.models import Doctor

# Create your tests here.


class DoctorViewSetTests(TestCase):
    def setUp(self):
        self.patient = Patient.objects.create(
            first_name="Patient",
            last_name="Patient",
            date_of_birth="1990-01-01",
            contact_number="12345678901",
            email="testPatient@example.com",
            address="123 Test St",
            medical_history="Description of medical history of the patient",
        )
        self.doctor = Doctor.objects.create(
            first_name="Doctor",
            last_name="Doctor",
            qualification="Test",
            contact_number="12345678901",
            email="testDoctor@example.com",
            address="123 Test St",
            biography="Description of the doctor's biography",
            is_on_vacation=False,
        )
        self.client = APIClient()

        # Create a user
        self.user = User.objects.create_user(
            username="testAdmin", password="testAdminPassword"
        )

        # Create the "doctors" group and add the user to it
        doctors_group, created = Group.objects.get_or_create(name="doctors")
        self.user.groups.add(doctors_group)

        # Authenticate the client
        self.client.login(username="testAdmin", password="testAdminPassword")

    def test_list_should_return_200(self):
        url = reverse("doctor-appointments", kwargs={"pk": self.doctor.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_set_on_vacation_should_return_200(self):
        url = reverse("doctor-set-on-vacation", kwargs={"pk": self.doctor.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_set_off_vacation_should_return_200(self):
        url = reverse("doctor-set-off-vacation", kwargs={"pk": self.doctor.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
