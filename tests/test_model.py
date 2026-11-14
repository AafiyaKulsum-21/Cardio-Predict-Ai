"""
Unit tests for model inference and serialization (Joblib & Pickle).
"""

import unittest
import os
import joblib
import pickle
import numpy as np


class TestModelInference(unittest.TestCase):

    def setUp(self):
        self.joblib_path = 'models/heart_disease_model.joblib'
        self.pickle_path = 'models/heart_disease_model.pkl'
        self.scaler_path = 'models/scaler.joblib'

        self.assertTrue(os.path.exists(self.joblib_path), "Joblib model file missing.")
        self.assertTrue(os.path.exists(self.pickle_path), "Pickle model file missing.")
        self.assertTrue(os.path.exists(self.scaler_path), "Scaler file missing.")

        self.joblib_model = joblib.load(self.joblib_path)
        with open(self.pickle_path, 'rb') as f:
            self.pickle_model = pickle.load(f)
        self.scaler = joblib.load(self.scaler_path)

        # Sample test input vector (13 features)
        self.sample_features = np.array([[55, 1, 2, 130, 230, 0, 1, 150, 0, 1.0, 2, 0, 2]])

    def test_joblib_and_pickle_consistency(self):
        scaled = self.scaler.transform(self.sample_features)
        pred_joblib = self.joblib_model.predict(scaled)
        pred_pickle = self.pickle_model.predict(scaled)

        prob_joblib = self.joblib_model.predict_proba(scaled)
        prob_pickle = self.pickle_model.predict_proba(scaled)

        self.assertEqual(pred_joblib[0], pred_pickle[0])
        np.testing.assert_allclose(prob_joblib, prob_pickle, rtol=1e-5)

    def test_prediction_output_bounds(self):
        scaled = self.scaler.transform(self.sample_features)
        pred = self.joblib_model.predict(scaled)[0]
        prob = self.joblib_model.predict_proba(scaled)[0, 1]

        self.assertIn(pred, [0, 1])
        self.assertTrue(0.0 <= prob <= 1.0)


if __name__ == '__main__':
    unittest.main()
