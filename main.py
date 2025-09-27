"""
Main application - simple orchestration of all components.

Simple function analysis system that:
1. Loads 3 CSV files into SQLite database
2. Selects 4 ideal functions using least squares
3. Matches test data to ideal functions
4. Creates visualization
"""

import sys
import os
from database import Database
from selector import FunctionSelector  
from tester import TestProcessor
from visualizer import Visualizer
from exceptions import FunctionAnalysisError

class SimpleFunctionAnalysis:
    """
    Main analysis system - coordinates all components.
    
    Simple approach with minimal complexity but full functionality.
    """
    
    def __init__(self, db_name="analysis.db"):
        """Initialize system components."""
        print("🔧 Initializing Function Analysis System...")
        self.db = Database(db_name)
        self.selector = FunctionSelector(self.db)
        self.tester = TestProcessor(self.db, self.selector)
        self.visualizer = Visualizer(self.db)
        print("✓ System ready")
    
    def run_analysis(self, training_csv, ideal_csv, test_csv, 
                    output_html="analysis_results.html"):
        """
        Run complete analysis pipeline.
        
        Args:
            training_csv: Training data file (x, y1, y2, y3, y4)
            ideal_csv: Ideal functions file (x, y1, y2, ..., y50)  
            test_csv: Test data file (x, y)
            output_html: Output visualization file
        """
        try:
            print("\n📊 Starting Function Analysis Pipeline")
            print("=" * 50)
            
            # Step 1: Load data
            print("1️⃣ Loading data into database...")
            self.db.load_training(training_csv)
            self.db.load_ideal(ideal_csv)
            
            # Step 2: Select ideal functions
            print("\n2️⃣ Selecting ideal functions...")
            selected = self.selector.process()
            
            # Step 3: Process test data
            print(f"\n3️⃣ Processing test data...")
            results = self.tester.process(test_csv)
            self.db.save_results(results)
            
            # Step 4: Create visualization
            print(f"\n4️⃣ Creating visualization...")
            self.visualizer.create_plots(selected, output_html)
            
            print("\n🎉 Analysis Complete!")
            print(f"📁 Database: analysis.db")
            print(f"📊 Visualization: {output_html}")
            print(f"🎯 Matched {len(results)} test points")
            
        except FunctionAnalysisError as e:
            print(f"❌ Analysis failed: {e}")
            sys.exit(1)


def main():
    """Main entry point."""
    print("🚀 Simple Function Analysis System")
    print("=" * 40)
    
    # Run analysis
    analyzer = SimpleFunctionAnalysis()
    analyzer.run_analysis(
        training_csv='dataset/train.csv',
        ideal_csv='dataset/ideal.csv',
        test_csv='dataset/test.csv'
    )

if __name__ == "__main__":
    main()
