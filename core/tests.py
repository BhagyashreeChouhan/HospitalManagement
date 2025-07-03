from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token

class PatientAPITestCase(TestCase):
    def setUp(self):
        # Create two doctors (users) and generate their tokens
        self.doctor_a = User.objects.create_user(username='geet', password='geet01')
        self.doctor_b = User.objects.create_user(username='rajesh', password='rajesh01')
        self.token_a = Token.objects.create(user=self.doctor_a)
        self.token_b = Token.objects.create(user=self.doctor_b)
        self.client = APIClient()

    def login_as(self, token):
        # Helper to set the Authorization header
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    def test_create_patient(self):
        self.login_as(self.token_a)
        patient_data = {
            'name': 'Amit Sharma',
            'age': 34,
            'gender': 'Male',
            'address': 'Milkman Colony, Jodhpur'
        }
        response = self.client.post('/api/patients/', patient_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], patient_data['name'])
        # Check created_by returns the username
        self.assertEqual(response.data['created_by'], self.doctor_a.username)

    def test_doctor_sees_only_own_patients(self):
        # Doctor A adds patient Priya
        self.login_as(self.token_a)
        self.client.post('/api/patients/', {
            'name': 'Priya', 'age': 28, 'gender': 'Female', 'address': 'Street 2'
        })
        # Doctor B adds patient Yash
        self.login_as(self.token_b)
        self.client.post('/api/patients/', {
            'name': 'Yash', 'age': 45, 'gender': 'Male', 'address': 'Block 10'
        })
        # Doctor B fetches list - should see only Yash
        list_resp_b = self.client.get('/api/patients/')
        patient_names_b = [p['name'] for p in list_resp_b.data]
        self.assertIn('Yash', patient_names_b)
        self.assertNotIn('Priya', patient_names_b)
        # Doctor A fetches list - should see only Priya
        self.login_as(self.token_a)
        list_resp_a = self.client.get('/api/patients/')
        patient_names_a = [p['name'] for p in list_resp_a.data]
        self.assertIn('Priya', patient_names_a)
        self.assertNotIn('Yash', patient_names_a)

    def test_doctor_cannot_view_other_doctors_records(self):
        # Doctor A creates patient and adds a record
        self.login_as(self.token_a)
        pat_resp = self.client.post('/api/patients/', {
            'name': 'Reena', 'age': 38, 'gender': 'Female', 'address': 'MG Road'
        })
        pid = pat_resp.data['id']
        record_data = {
            'patient': pid, 'symptoms': 'Fever', 'diagnosis': 'Flu', 'treatment': 'Rest'
        }
        self.client.post('/api/patients/records/add', record_data)

        # Doctor B tries to view Doctor A's patient's records - should get 403
        self.login_as(self.token_b)
        record_resp = self.client.get(f'/api/patients/{pid}/records/')
        self.assertEqual(record_resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_access_is_denied(self):
        self.client.credentials()  # clears any auth
        resp = self.client.get('/api/patients/')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
