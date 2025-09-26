"""
Simple unit tests for the function analysis system.

Basic tests to verify core functionality works.
"""

import unittest
import tempfile
import os
import pandas as pd
import numpy as np
from database import Database
from selector import FunctionSelector
from exceptions import DataError, SelectionError

class TestSimpleAnalysis(unittest.TestCase):
    """Simple tests for the analysis system."""
    
    def setUp(self):
        """Create temporary test database."""
        self.test_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.test_db.close()
        self.db = Database(self.test_db.name)
        
        # Create simple test data
        self.test_data = pd.DataFrame({
            'x': [1, 2, 3, 4],
            'y1': [1, 4, 9, 16],  # x^2
            'y2': [1, 2, 3, 4],   # x
            'y3': [2, 4, 6, 8],   # 2x
            'y4': [0, 1, 2, 3]    # x-1
        })
    
    def tearDown(self):
        """Clean up test files."""
        try:
            os.unlink(self.test_db.name)
        except:
            pass
    
    def test_database_operations(self):
        """Test basic database operations."""
        # Create temp CSV
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            self.test_data.to_csv(f.name, index=False)
            temp_csv = f.name
        
        try:
            # Test loading
            self.db.load_training(temp_csv)
            retrieved = self.db.get_training()
            
            # Verify data loaded correctly
            self.assertEqual(len(retrieved), 4)
            self.assertTrue(all(col in retrieved.columns for col in ['x', 'y1', 'y2', 'y3', 'y4']))
        finally:
            os.unlink(temp_csv)
    
    def test_function_selection(self):
        """Test ideal function selection."""
        # Load test data
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            self.test_data.to_csv(f.name, index=False)
            self.db.load_training(f.name)
            os.unlink(f.name)
        
        # Create ideal functions (y1 should match training y1 closely)
        ideal_data = self.test_data.copy()
        ideal_data['y5'] = [1.1, 4.1, 9.1, 16.1]  # Close to y1
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            ideal_data.to_csv(f.name, index=False)
            self.db.load_ideal(f.name)
            os.unlink(f.name)
        
        # Test selection
        selector = FunctionSelector(self.db)
        selected = selector.process()
        
        # Should select 4 functions
        self.assertEqual(len(selected), 4)
        self.assertIn('y1', selected)
    
    def test_custom_exceptions(self):
        """Test custom exceptions work."""
        with self.assertRaises(DataError):
            self.db.load_training('nonexistent_file.csv')
    
    def test_data_cleaning(self):
        """Test data cleaning functionality."""
        from processor import BaseProcessor
        
        class TestProcessor(BaseProcessor):
            def process(self):
                pass
        
        processor = TestProcessor()
        
        # Data with NaN and duplicates
        dirty_data = pd.DataFrame({
            'x': [1, 2, np.nan, 2, 3],
            'y': [1, 2, 3, 2, 4]
        })
        
        cleaned = processor.clean_data(dirty_data)
        
        # Should remove NaN and duplicate
        self.assertEqual(len(cleaned), 3)
        self.assertFalse(cleaned.isnull().any().any())

def run_tests():
    """Run the test suite."""
    unittest.main(verbosity=2)

if __name__ == '__main__':
    run_tests()