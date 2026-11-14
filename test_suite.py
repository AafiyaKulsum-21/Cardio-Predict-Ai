"""
CardioPredict AI: Comprehensive Test Runner
Executes all unit and integration tests.
Usage:
    python test_suite.py
"""

import unittest
import sys

if __name__ == '__main__':
    print("=" * 65)
    print("      CARDIOPREDICT AI: EXECUTING FULL TEST SUITE")
    print("=" * 65)

    loader = unittest.TestLoader()
    suite = loader.discover('tests', pattern='test_*.py')

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if result.wasSuccessful():
        print("\n[SUCCESS] All unit and integration tests passed cleanly!")
        sys.exit(0)
    else:
        print(f"\n[FAIL] {len(result.failures)} test(s) failed, {len(result.errors)} error(s).")
        sys.exit(1)
