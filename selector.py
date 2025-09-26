import numpy as np
from processor import BaseProcessor
from exceptions import SelectionError

class FunctionSelector(BaseProcessor):
    """
    Select ideal functions using least squares criterion
    
    For each training function, find the ideal function with minimum sum of squared errors.
    """

    def __init__(self, database):
        """Initialize with database"""
        self.db = database
        self.selected = {}
    
    def process(self):
        """
        Select ideal functions and training functions

        Returns:
            dict: Mapping of training function to ideal function
        """

        try:
            training = self.clean_data(self.db.get_training())
            ideal = self.clean_data(self.db.get_ideal())

            print("Selecting ideal functions...")

            for train_col in ['y1', 'y2', 'y3', 'y4']:
                best_error = float('inf')
                best_ideal = None
                
                # Test each ideal function
                for i in range(1, 51):
                    ideal_col = f'y{i}'
                    if ideal_col in ideal.columns:
                        # Calculate least squares error
                        error = np.sum((training[train_col] - ideal[ideal_col]) ** 2)
                        if error < best_error:
                            best_error = best_error
                            best_ideal = i
                
                if best_ideal:
                    self.selected[train_col] = best_ideal
                    print(f"  {train_col} -> y{best_ideal} (error: {best_error:.3f})")
            
            if len(self.selected) != 4:
                raise SelectionError("Could not select 4 ideal functions")
                
            return self.selected
            
        except Exception as e:
            raise SelectionError(f"Function selection failed: {e}")