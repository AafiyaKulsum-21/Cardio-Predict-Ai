"""
Unit tests for data preprocessing module.
"""

import unittest
import numpy as np
import pandas as pd
from src.data_preprocessing import (
    load_dataset, validate_and_clean_data,
    prepare_train_test_data, FEATURE_NAMES, TARGET_NAME
)


class TestDataPreprocessing(unittest.TestCase):

    def setUp(self):
        self.df = load_dataset('data/heart.csv')

    def test_dataset_loaded(self):
        self.assertFalse(self.df.empty)
        self.assertGreater(len(self.df), 100)
        for col in FEATURE_NAMES + [TARGET_NAME]:
            self.assertIn(col, self.df.columns)

    def test_cleaning_drops_duplicates(self):
        cleaned = validate_and_clean_data(self.df)
        self.assertLessEqual(len(cleaned), len(self.df))
        self.assertEqual(cleaned.isnull().sum().sum(), 0)

    def test_train_test_split_shapes(self):
        cleaned = validate_and_clean_data(self.df)
        X_tr, X_te, y_tr, y_te, X_tr_sc, X_te_sc, scaler = prepare_train_test_data(cleaned, test_size=0.2)
        
        self.assertEqual(len(X_tr) + len(X_te), len(cleaned))
        self.assertEqual(X_tr_sc.shape[1], len(FEATURE_NAMES))
        self.assertEqual(X_te_sc.shape[1], len(FEATURE_NAMES))
        # Scaled mean should be close to 0 and std close to 1
        np.testing.assert_allclose(X_tr_sc.mean(axis=0), 0, atol=1e-1)


if __name__ == '__main__':
    unittest.main()
