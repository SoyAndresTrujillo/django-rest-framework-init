from rest_framework.routers import DefaultRouter

from .viewsets import (
    ListPatientView,
    ListMedicalRecordView,
)

router = DefaultRouter()
router.register("patients", ListPatientView)
router.register("medicalrecords", ListMedicalRecordView)

urlpatterns = router.urls
