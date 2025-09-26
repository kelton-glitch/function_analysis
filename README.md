# Simple Function Analysis System

Dead simple but complete function analysis system with modular design.

## What it does:
1. **Loads 3 CSV files** (training, ideal, test) into SQLite database
2. **Selects 4 ideal functions** using least squares criterion  
3. **Matches test data** to ideal functions with √2 deviation rule
4. **Creates interactive visualization** with Bokeh

## Files needed:
- `training.csv` - x, y1, y2, y3, y4 columns
- `ideal.csv` - x, y1, y2, ..., y50 columns  
- `test.csv` - x, y columns

## Usage:

### Run with sample data:
```bash
python main.py
```

### Run with your data:
```python
from main import SimpleFunctionAnalysis

analyzer = SimpleFunctionAnalysis()
analyzer.run_analysis(
    training_csv='your_training.csv',
    ideal_csv='your_ideal.csv', 
    test_csv='your_test.csv'
)
```

### Run tests:
```bash
python test_simple.py
```

## Architecture:

**Modular but simple:**
- `database.py` - SQLite operations
- `selector.py` - Function selection (inherits from BaseProcessor)  
- `tester.py` - Test processing (inherits from BaseProcessor)
- `visualizer.py` - Bokeh plots
- `processor.py` - Base class with inheritance
- `exceptions.py` - Custom exceptions
- `main.py` - Simple orchestration

## Output:
- `analysis.db` - SQLite database with all data
- `analysis_results.html` - Interactive visualization

**Just run `python main.py` and it works!** 🚀