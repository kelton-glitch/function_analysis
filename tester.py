import pandas as pd
import numpy as np
from processor import BaseProcessor
from exceptions import DataError

class TestProcessor(BaseProcessor):
    """
    Process test data and match to ideal functions.
    
    Uses sqrt(2) * training_deviation as acceptance criterion.
    """
    
    def __init__(self, database, selector):
        """Initialize with database and function selector."""
        self.db = database
        self.selector = selector
    
    def process(self, test_csv):
        """
        Process test data from CSV file.
        
        Args:
            test_csv: Path to test data CSV file
            
        Returns:
            list: Test results with matched ideal functions
        """
        try:
            # Load test data
            test_df = pd.read_csv(test_csv)
            test_df = self.clean_data(test_df)
            
            if not all(col in test_df.columns for col in ['x', 'y']):
                raise DataError("Test CSV missing 'x' or 'y' columns")
            
            # Get reference data
            training = self.db.get_training()
            ideal = self.db.get_ideal()
            selected = self.selector.selected
            
            if not selected:
                raise DataError("No ideal functions selected")
            
            results = []
            print(f"Processing {len(test_df)} test points...")
            
            for _, test_row in test_df.iterrows():
                result = self._match_point(test_row, selected, training, ideal)
                if result:
                    results.append(result)
            
            print(f"✓ Matched {len(results)} test points")
            return results
            
        except Exception as e:
            raise DataError(f"Test processing failed: {e}")
    
    def _match_point(self, test_row, selected, training, ideal):
        """Match a single test point to ideal functions."""
        test_x, test_y = test_row['x'], test_row['y']
        best_match = None
        min_deviation = float('inf')
        
        # Check each selected ideal function
        for train_func, ideal_idx in selected.items():
            ideal_col = f'y{ideal_idx}'
            
            # Find closest x value
            x_diff = np.abs(ideal['x'] - test_x)
            closest_idx = x_diff.idxmin()
            
            ideal_y = ideal.loc[closest_idx, ideal_col]
            deviation = abs(test_y - ideal_y)
            
            # Calculate max allowed deviation (sqrt(2) criterion)
            train_x_diff = np.abs(training['x'] - test_x)
            train_closest_idx = train_x_diff.idxmin()
            train_y = training.loc[train_closest_idx, train_func]
            train_deviation = abs(train_y - ideal_y)
            max_deviation = np.sqrt(2) * train_deviation
            
            # Check if point meets criterion and is best match
            if deviation <= max_deviation and deviation < min_deviation:
                min_deviation = deviation
                best_match = {
                    'x': test_x,
                    'y': test_y,
                    'ideal_function': ideal_col,
                    'deviation': deviation
                }
        
        return best_match