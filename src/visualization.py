"""
Visualization Module for Education Policy Dashboard
Creates interactive and static visualizations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as pyo


class EducationVisualizer:
    """Create visualizations for education policy insights"""
    
    def __init__(self, df=None, output_dir='visualizations'):
        self.df = df
        self.output_dir = output_dir
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # Set style
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 6)
    
    def plot_state_comparison(self, metric_col, title="State-wise Comparison", 
                             top_n=10, ascending=False):
        """Create bar chart comparing states on a metric"""
        if self.df is None or metric_col not in self.df.columns:
            return None
        
        # Find state column
        state_col = None
        for col in ['State', 'state', 'STATE', 'State_Name']:
            if col in self.df.columns:
                state_col = col
                break
        
        if not state_col:
            return None
        
        # Aggregate by state
        state_data = self.df.groupby(state_col)[metric_col].sum().reset_index()
        state_data = state_data.sort_values(metric_col, ascending=ascending).head(top_n)
        
        # Create plotly figure
        fig = px.bar(state_data, x=state_col, y=metric_col,
                    title=title,
                    labels={state_col: 'State', metric_col: metric_col.replace('_', ' ').title()},
                    color=metric_col,
                    color_continuous_scale='Viridis')
        
        fig.update_layout(
            xaxis_tickangle=-45,
            height=600,
            showlegend=False
        )
        
        fig.write_html(f"{self.output_dir}/state_comparison_{metric_col}.html")
        return fig
    
    def plot_district_heatmap(self, metric_col, state_col='State'):
        """Create heatmap showing district performance"""
        if self.df is None:
            return None
        
        # Find district column
        district_col = None
        for col in ['District', 'district', 'DISTRICT', 'District_Name']:
            if col in self.df.columns:
                district_col = col
                break
        
        if not district_col:
            return None
        
        # Create pivot table
        pivot_data = self.df.pivot_table(
            values=metric_col,
            index=state_col,
            columns=district_col,
            aggfunc='mean'
        )
        
        # Create heatmap
        fig = px.imshow(pivot_data,
                       labels=dict(x="District", y="State", color=metric_col),
                       title=f"District-wise {metric_col.replace('_', ' ').title()} Heatmap",
                       color_continuous_scale='RdYlGn_r')
        
        fig.write_html(f"{self.output_dir}/district_heatmap_{metric_col}.html")
        return fig
    
    def plot_gender_parity(self, girls_col=None, boys_col=None):
        """Visualize gender parity across states/districts"""
        if self.df is None:
            return None
        
        # Find gender columns
        if girls_col is None:
            girls_col = [col for col in self.df.columns if 'girl' in col.lower() or 'female' in col.lower()]
        if boys_col is None:
            boys_col = [col for col in self.df.columns if 'boy' in col.lower() or 'male' in col.lower()]
        
        if not girls_col or not boys_col:
            return None
        
        # Find state column
        state_col = None
        for col in ['State', 'state', 'STATE', 'State_Name']:
            if col in self.df.columns:
                state_col = col
                break
        
        if not state_col:
            return None
        
        # Calculate GPI by state
        state_gender = self.df.groupby(state_col).agg({
            girls_col[0] if isinstance(girls_col, list) else girls_col: 'sum',
            boys_col[0] if isinstance(boys_col, list) else boys_col: 'sum'
        }).reset_index()
        
        state_gender['GPI'] = state_gender[girls_col[0] if isinstance(girls_col, list) else girls_col] / \
                             (state_gender[boys_col[0] if isinstance(boys_col, list) else boys_col] + 1e-10)
        
        # Create visualization
        fig = px.bar(state_gender, x=state_col, y='GPI',
                    title='Gender Parity Index by State',
                    labels={'GPI': 'Gender Parity Index (Girls/Boys)', state_col: 'State'},
                    color='GPI',
                    color_continuous_scale='RdYlGn',
                    color_continuous_midpoint=1.0)
        
        # Add reference line at 1.0
        fig.add_hline(y=1.0, line_dash="dash", line_color="red", 
                     annotation_text="Parity Line")
        
        fig.update_layout(height=600, xaxis_tickangle=-45)
        fig.write_html(f"{self.output_dir}/gender_parity.html")
        return fig
    
    def plot_facility_coverage(self, facility_cols=None):
        """Visualize facility coverage across regions"""
        if self.df is None:
            return None
        
        if facility_cols is None:
            facility_cols = [col for col in self.df.columns if any(keyword in col.lower() 
                           for keyword in ['toilet', 'water', 'library', 'computer', 'internet'])]
        
        if not facility_cols:
            return None
        
        # Find state column
        state_col = None
        for col in ['State', 'state', 'STATE', 'State_Name']:
            if col in self.df.columns:
                state_col = col
                break
        
        if not state_col:
            return None
        
        # Calculate coverage percentage by state
        facility_coverage = []
        for facility in facility_cols[:5]:  # Limit to 5 facilities
            state_facility = self.df.groupby(state_col).agg({
                facility: lambda x: (x > 0).sum() if x.dtype in ['int64', 'float64'] else x.notna().sum()
            }).reset_index()
            state_facility['total_schools'] = self.df.groupby(state_col).size().values
            state_facility['coverage_pct'] = (state_facility[facility] / state_facility['total_schools'] * 100)
            state_facility['facility'] = facility
            facility_coverage.append(state_facility)
        
        coverage_df = pd.concat(facility_coverage, ignore_index=True)
        
        # Create grouped bar chart
        fig = px.bar(coverage_df, x=state_col, y='coverage_pct', color='facility',
                    title='Facility Coverage by State',
                    labels={'coverage_pct': 'Coverage Percentage (%)', state_col: 'State'},
                    barmode='group')
        
        fig.update_layout(height=600, xaxis_tickangle=-45)
        fig.write_html(f"{self.output_dir}/facility_coverage.html")
        return fig
    
    def plot_teacher_student_ratio(self):
        """Visualize teacher-student ratio across regions"""
        if self.df is None:
            return None
        
        # This will be implemented based on actual data structure
        # Placeholder for now
        pass
    
    def create_dashboard(self, output_file='dashboard.html'):
        """Create an interactive dashboard combining multiple visualizations"""
        if self.df is None:
            return None
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('State Comparison', 'Gender Parity', 
                          'Facility Coverage', 'District Performance'),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "bar"}, {"type": "scatter"}]]
        )
        
        # Add visualizations (placeholder - to be filled based on actual data)
        
        fig.update_layout(
            title_text="Education Policy Dashboard",
            height=1000,
            showlegend=True
        )
        
        fig.write_html(f"{self.output_dir}/{output_file}")
        return fig
    
    def plot_trend_analysis(self, year_col=None, metric_col=None):
        """Analyze trends over years (if multiple years of data available)"""
        if self.df is None:
            return None
        
        # This will compare 2023-24 vs 2024-25 data
        pass


if __name__ == "__main__":
    # Example usage
    visualizer = EducationVisualizer()
    # visualizer.plot_state_comparison('Total_Students')

