from django.urls import path
from .views import RegisterAPI, LoginAPI, PatientListCreateView, MedicalReportCreateView, MedicalReportListView, api_root

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name="register"),
    path('login/', LoginAPI.as_view(), name="login"),
    path('patients/', PatientListCreateView.as_view(), name='patients'),
    path('patients/records/add', MedicalReportCreateView.as_view(), name='add_record'),
    path('patients/<int:pk>/records/', MedicalReportListView.as_view(), name='patient_records'),
]