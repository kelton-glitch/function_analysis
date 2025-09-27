from bokeh.plotting import figure, show, output_file
from bokeh.layouts import column
from bokeh.models import HoverTool

class Visualizer:
    """
    Create simple visualizations with Bokeh.
    
    Shows training data, ideal functions, and test results.
    """
    
    def __init__(self, database):
        """Initialize with database."""
        self.db = database
    
    def create_plots(self, selected_functions, output_file_name="results.html"):
        """
        Create visualization plots.
        
        Args:
            selected_functions: Dictionary of selected ideal functions
            output_file_name: Name of HTML output file
        """
        output_file(output_file_name)
        
        # Get data
        training = self.db.get_training()
        ideal = self.db.get_ideal()
        results = self.db.get_results()
        
        plots = []
        
        # Training data plot
        p1 = figure(title="Training Functions", width=600, height=400,
                   x_axis_label="x", y_axis_label="y")
        
        colors = ['red', 'blue', 'green', 'orange']
        for i, col in enumerate(['y1', 'y2', 'y3', 'y4']):
            p1.line(training['x'], training[col], 
                   legend_label=f"Training {col}", 
                   color=colors[i], line_width=2)
        p1.legend.click_policy = "hide"
        plots.append(p1)
        
        # Selected ideal functions plot
        p2 = figure(title="Selected Ideal Functions", width=600, height=400,
                   x_axis_label="x", y_axis_label="y")
        
        for i, (train_func, ideal_idx) in enumerate(selected_functions.items()):
            ideal_col = f'y{ideal_idx}'
            if ideal_col in ideal.columns:
                p2.line(ideal['x'], ideal[ideal_col],
                       legend_label=f"Ideal y{ideal_idx} (for {train_func})",
                       color=colors[i], line_width=2)
        p2.legend.click_policy = "hide"
        plots.append(p2)
        
        # Test results plot
        if not results.empty:
            p3 = figure(title="Test Results", width=600, height=400,
                       x_axis_label="x", y_axis_label="y")
            
            # Add hover tool
            hover = HoverTool(tooltips=[
                ("X", "@x"),
                ("Y", "@y")
            ])
            p3.add_tools(hover)
            
            p3.circle(results['x'], results['y'], size=8, alpha=0.7,
                     color='purple', legend_label="Test Points")
            plots.append(p3)
        
        # Show all plots
        layout = column(*plots)
        show(layout)
        print(f"✓ Visualization saved to {output_file_name}")