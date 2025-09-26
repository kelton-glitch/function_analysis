class FunctionAnalysisError(Exception):
    """Base exception for function analysis"""
    pass

class DataError(FunctionAnalysisError):
    """Error loading or processing data"""
    pass

class SelectionError(FunctionAnalysisError):
    """Error selecting ideal functions."""
    pass
