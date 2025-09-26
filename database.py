import pandas as pd
import numpy as np
from sqlalchemy import create_engine, Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from exceptions import DataError

Base = declarative_base()

class TrainingData(Base):
    """Training data table."""
    __tablename__ = 'training'
    id = Column(Integer, primary_key=True)
    x = Column(Float)
    y1 = Column(Float)
    y2 = Column(Float)
    y3 = Column(Float)
    y4 = Column(Float)

class IdealFunction(Base):
    """Ideal functions table (dynamic columns added)."""
    __tablename__ = 'ideal'
    id = Column(Integer, primary_key=True)
    x = Column(Float)

class TestResult(Base):
    """Test results table."""
    __tablename__ = 'results'
    id = Column(Integer, primary_key=True)
    x = Column(Float)
    y = Column(Float)
    ideal_function = Column(String)
    deviation = Column(Float)

class Database:
    """
    Simple database manager.
    
    Handles loading CSV data into SQLite and retrieving it.
    """
    
    def __init__(self, db_name="analysis.db"):
        """Initialize database."""
        self.engine = create_engine(f'sqlite:///{db_name}')
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)
        self._add_ideal_columns()
    
    def _add_ideal_columns(self):
        """Add y1-y50 columns to ideal table."""
        with self.engine.connect() as conn:
            for i in range(1, 51):
                try:
                    conn.execute(f"ALTER TABLE ideal ADD COLUMN y{i} FLOAT")
                except:
                    pass  # Column exists
    
    def load_training(self, csv_file):
        """
        Load training data from CSV.
        
        Args:
            csv_file: Path to training CSV file
        """
        try:
            df = pd.read_csv(csv_file)
            # Validate columns
            required = ['x', 'y1', 'y2', 'y3', 'y4']
            if not all(col in df.columns for col in required):
                raise DataError(f"Training CSV missing columns: {required}")
            
            df.to_sql('training', self.engine, if_exists='replace', index=False)
            print(f"✓ Loaded {len(df)} training records")
        except Exception as e:
            raise DataError(f"Failed to load training data: {e}")
    
    def load_ideal(self, csv_file):
        """
        Load ideal functions from CSV.
        
        Args:
            csv_file: Path to ideal functions CSV file
        """
        try:
            df = pd.read_csv(csv_file)
            if 'x' not in df.columns:
                raise DataError("Ideal CSV missing 'x' column")
            
            df.to_sql('ideal', self.engine, if_exists='replace', index=False)
            print(f"✓ Loaded {len(df)} ideal function records")
        except Exception as e:
            raise DataError(f"Failed to load ideal functions: {e}")
    
    def get_training(self):
        """Get training data as DataFrame."""
        return pd.read_sql('SELECT * FROM training', self.engine)
    
    def get_ideal(self):
        """Get ideal functions as DataFrame."""
        return pd.read_sql('SELECT * FROM ideal', self.engine)
    
    def save_results(self, results):
        """Save test results to database."""
        df = pd.DataFrame(results)
        df.to_sql('results', self.engine, if_exists='replace', index=False)
        print(f"✓ Saved {len(results)} test results")
    
    def get_results(self):
        """Get test results as DataFrame."""
        try:
            return pd.read_sql('SELECT * FROM results', self.engine)
        except:
            return pd.DataFrame()