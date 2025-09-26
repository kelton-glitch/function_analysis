from abc import ABC, abstractmethod
import pandas from pandas

class BaseProcessor(ABC):
    """
    Base class for data processing.
    
    Provides common functionality like data cleaning.
    """

    def clean_data(self, df):
        """Remove NaN values and duplicates"""
        original_len = len(df)
        df_clean = df.dropna().drop_duplicates()
        removed = original_len - len(df_clean)
        if removed > 0:
            print(f" Cleaned data: removed {removed} invalid rows")
        return df_clean
    
    @abstractmethod
    def process(self, *args, **kwargs):
        """Process data"""
        pass
    