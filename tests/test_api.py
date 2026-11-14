"""
Unit and integration tests for Flask Web Application & REST API endpoints.
"""

import unittest
import json
from app.app import app


class TestFlaskAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        self.valid_payload = {
            "age": 55,
            "sex": 1,
            "cp": 2,
            "trestbps": 130,
            "chol": 230,
            "fbs": 0,
            "restecg": 1,
            "thalach": 150,
            "exang": 0,
            "oldpeak": 1.0,
            "slope": 2,
            "ca": 0,
            "thal": 2
        }

    def test_health_endpoint(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertTrue(data['model_loaded'])
        self.assertTrue(data['scaler_loaded'])

    def test_home_page_renders(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'CardioPredict', response.data)
        self.assertIn(b'Clinical Decision Support System', response.data)

    def test_model_info_endpoint(self):
        response = self.app.get('/api/models/info')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('metadata', data)
        self.assertEqual(data['metadata']['model_name'], 'Random Forest Classifier')

    def test_api_predict_success(self):
        response = self.app.post(
            '/api/predict',
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('prediction', data)
        self.assertIn('probability', data)
        self.assertIn('risk_level', data)
        self.assertIn('recommendations', data)
        self.assertIn(data['prediction'], [0, 1])

    def test_api_predict_missing_feature(self):
        incomplete_payload = self.valid_payload.copy()
        del incomplete_payload['age']

        response = self.app.post(
            '/api/predict',
            data=json.dumps(incomplete_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertIn('Missing required biomarker fields', data['message'])

    def test_web_form_predict(self):
        response = self.app.post('/predict', data=self.valid_payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Cardiovascular Risk Report', response.data)
        self.assertIn(b'Heart Disease Probability', response.data)


if __name__ == '__main__':
    unittest.main()
