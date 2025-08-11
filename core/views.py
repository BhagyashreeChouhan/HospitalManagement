from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer, PatientSerializer, MedicalRecordSerializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import generics, permissions
from .models import Patient, MedicalRecord
from .permissions import DoctorOrAdminPermission
from rest_framework.authentication import TokenAuthentication
from django.core.exceptions import PermissionDenied

# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def api_root(request):
    return Response({
        "message": "Hospital Management API",
        "endpoints": {
            "register": "/api/register/",
            "login": "/api/login/",
            "patients": "/api/patients/",
            "add_record": "/api/patients/records/add",
            "patient_records": "/api/patients/<id>/records/"
        }
    })

class RegisterAPI(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message":"Account created",
                "data": serializer.data
            }, status=201)
        return Response({
                "message":"Account not created",
                "data": serializer.errors
            }, status=400)
    
class LoginAPI(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.validated_data['username'],
                                password = serializer.validated_data['password'])
            if user is None:
                return Response({
                "message":"Invalid credentials.",
                "data": {}
            }, status=401)
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "message":"Login successful",
                "token": token.key
            }, status=200)
        return Response({
                "message":"Keys missing or invalid data.",
                "data":serializer.errors
            }, status=400)

# Patients - list and add
class PatientListCreateView(generics.ListCreateAPIView):
    serializer_class = PatientSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, DoctorOrAdminPermission]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Patient.objects.all()
        return Patient.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

# Medical Records - add
class MedicalReportCreateView(generics.CreateAPIView):
    serializer_class = MedicalRecordSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        patient_id = self.request.data.get('patient')
        patient = Patient.objects.get(id=patient_id)
        # Check doctor owns patient
        if not self.request.user.is_superuser and patient.created_by != self.request.user:
            raise PermissionDenied("You cannot add records to this patient.")
        serializer.save(patient=patient)

# Medical Records - list
class MedicalReportListView(generics.ListAPIView):
    serializer_class = MedicalRecordSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, DoctorOrAdminPermission]

    def get_queryset(self):
        patient_id = self.kwargs['pk']
        patient = Patient.objects.get(id=patient_id)
        self.check_object_permissions(self.request, patient)
        return MedicalRecord.objects.filter(patient=patient)
