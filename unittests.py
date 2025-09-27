import unittest
import pandas as pd
import numpy as np
import os

# Import your modules
from database import Database
from selector import FunctionSelector
from exceptions import DataError, SelectionError
from processor import BaseProcessor


class TestBasics(unittest.TestCase):
    """Simple tests for basic functionality."""
    
    def setUp(self):
        """Create a test database."""
        self.db = Database("test.db")
    
    def tearDown(self):
        """Clean up test database."""
        try:
            os.remove("test.db")
        except:
            pass  # Ignore if file doesn't exist
    
    def test_database_creation(self):
        """Test that database is created."""
        self.assertTrue(os.path.exists("test.db"))
    
    def test_custom_exceptions(self):
        """Test custom exceptions work."""
        with self.assertRaises(DataError):
            self.db.load_training("fake_file.csv")
    
    def test_data_cleaning(self):
        """Test data cleaning removes bad data."""
        class SimpleProcessor(BaseProcessor):
            def process(self):
                pass
        
        processor = SimpleProcessor()
        
        # Data with NaN and duplicates
        dirty_data = pd.DataFrame({
            'x': [1, 2, np.nan, 2, 3],
            'y': [1, 2, 3, 2, 4]
        })
        
        cleaned = processor.clean_data(dirty_data)
        
        # Should be smaller after cleaning
        self.assertLess(len(cleaned), len(dirty_data))
        # Should have no NaN values
        self.assertFalse(cleaned.isnull().any().any())


class TestWithSampleData(unittest.TestCase):
    """Tests using the sample data files."""
    
    def setUp(self):
        """Create database and sample data."""
        self.db = Database("test2.db")
        
        # Create simple sample data
        x = [1, 2, 3, 4, 5]
        
        # Training data
        training_data = pd.DataFrame({
            'x': x,
            'y1': [i**2 for i in x],      # x^2
            'y2': [i*2 for i in x],       # 2x  
            'y3': [i+1 for i in x],       # x+1
            'y4': [i*3 for i in x]        # 3x
        })
        training_data.to_csv('test_training.csv', index=False)
        
        # Ideal data (similar to training)
        ideal_data = pd.DataFrame({
            'x': x,
            'y1': [i**2 + 0.1 for i in x],    # Close to training y1
            'y2': [i*2 + 0.1 for i in x],     # Close to training y2
            'y3': [i+1 + 0.1 for i in x],     # Close to training y3
            'y4': [i*3 + 0.1 for i in x],     # Close to training y4
            'y5': [i*10 for i in x]           # Different function
        })
        ideal_data.to_csv('test_ideal.csv', index=False)
        
        # Test data
        test_data = pd.DataFrame({
            'x': [1.5, 2.5, 3.5],
            'y': [2.25, 6.25, 12.25]  # Should match y1 pattern
        })
        test_data.to_csv('test_data.csv', index=False)
    
    def tearDown(self):
        """Clean up files."""
        files_to_remove = ['test2.db', 'test_training.csv', 'test_ideal.csv', 'test_data.csv']
        for file in files_to_remove:
            try:
                os.remove(file)
            except:
                pass
    
    def test_load_training_data(self):
        """Test loading training data."""
        self.db.load_training('test_training.csv')
        data = self.db.get_training()
        
        # Should have 5 rows and required columns
        self.assertEqual(len(data), 5)
        self.assertIn('x', data.columns)
        self.assertIn('y1', data.columns)
        self.assertIn('y4', data.columns)
    
    def test_load_ideal_data(self):
        """Test loading ideal functions."""
        self.db.load_ideal('test_ideal.csv')
        data = self.db.get_ideal()
        
        # Should have data
        self.assertGreater(len(data), 0)
        self.assertIn('x', data.columns)
    
    def test_function_selection(self):
        """Test selecting ideal functions."""
        # Load data
        self.db.load_training('test_training.csv')
        self.db.load_ideal('test_ideal.csv')
        
        # Test selection
        selector = FunctionSelector(self.db)
        selected = selector.process()
        
        # Should select 4 functions
        self.assertEqual(len(selected), 4)
        
        # Should have selections for each training function
        for key in ['y1', 'y2', 'y3', 'y4']:
            self.assertIn(key, selected)
    
    def test_complete_workflow(self):
        """Test the complete workflow works."""
        try:
            # Load all data
            self.db.load_training('test_training.csv')
            self.db.load_ideal('test_ideal.csv')
            
            # Select functions
            selector = FunctionSelector(self.db)
            selected = selector.process()
            
            # This should work without errors
            self.assertIsInstance(selected, dict)
            self.assertGreater(len(selected), 0)
            
        except Exception as e:
            self.fail(f"Complete workflow failed: {e}")


def run_simple_tests():
    """Run the tests with simple output."""
    print("🧪 Running Simple Tests")
    print("=" * 30)
    
    # Run tests
    unittest.main(verbosity=2, exit=False)


if __name__ == '__main__':
    run_simple_tests()