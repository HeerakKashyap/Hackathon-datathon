
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA


class EducationPolicyAnalyzer:
    """Analyze education data for policy insights"""
    
    def __init__(self, data_path=None, df=None):
        if df is not None:
            self.df = df
        elif data_path:
            self.df = pd.read_csv(data_path)
        else:
            self.df = None
    
    def calculate_enrolment_metrics(self, state_col='State', district_col='District', 
                                   gender_cols=None, class_cols=None):
        """Calculate enrolment-related metrics"""
        if self.df is None:
            return None
        
        metrics = {}
        
        if gender_cols is None:
            gender_cols = [col for col in self.df.columns if 'girl' in col.lower() or 
                          'female' in col.lower() or 'boy' in col.lower() or 'male' in col.lower()]

        if len(gender_cols) >= 2:
            girls_col = [col for col in gender_cols if 'girl' in col.lower() or 'female' in col.lower()]
            boys_col = [col for col in gender_cols if 'boy' in col.lower() or 'male' in col.lower()]
            
            if girls_col and boys_col:
                girls_total = self.df[girls_col[0]].sum() if len(girls_col) == 1 else self.df[girls_col].sum(axis=1)
                boys_total = self.df[boys_col[0]].sum() if len(boys_col) == 1 else self.df[boys_col].sum(axis=1)
                
                metrics['gender_parity_index'] = girls_total / (boys_total + 1e-10)  # Avoid division by zero
        
  
        if state_col in self.df.columns:
            state_enrolment = self.df.groupby(state_col).size()
            metrics['state_enrolment'] = state_enrolment

        if district_col in self.df.columns:
            district_enrolment = self.df.groupby([state_col, district_col]).size()
            metrics['district_enrolment'] = district_enrolment
        
        return metrics
    
    def calculate_teacher_student_ratio(self, teacher_col='Total_Teachers', 
                                       student_col='Total_Students'):
        """Calculate teacher-student ratio by state/district"""
        if self.df is None:
            return None
        

        teacher_cols = [col for col in self.df.columns if 'teacher' in col.lower()]
        student_cols = [col for col in self.df.columns if 'student' in col.lower() or 
                       'enrolment' in col.lower() or 'enrolled' in col.lower()]
        
        if not teacher_cols or not student_cols:
            return None
        

        state_col = None
        for col in ['State', 'state', 'STATE', 'State_Name']:
            if col in self.df.columns:
                state_col = col
                break
        
        if state_col:
            aggregated = self.df.groupby(state_col).agg({
                teacher_cols[0]: 'sum',
                student_cols[0]: 'sum'
            })
            
            aggregated['TSR'] = aggregated[student_cols[0]] / (aggregated[teacher_cols[0]] + 1e-10)
            return aggregated
        
        return None
    
    def analyze_facility_availability(self, facility_cols=None):
        """Analyze availability of facilities (toilets, drinking water, etc.)"""
        if self.df is None:
            return None
        
        if facility_cols is None:
            facility_cols = [col for col in self.df.columns if any(keyword in col.lower() 
                           for keyword in ['toilet', 'water', 'library', 'computer', 'internet', 'electricity'])]
        
        facility_analysis = {}
        
        for col in facility_cols:
            if self.df[col].dtype in ['object', 'string']:
                
                facility_analysis[col] = self.df[col].value_counts()
            else:
                
                total = len(self.df)
                available = (self.df[col] > 0).sum() if self.df[col].dtype in ['int64', 'float64'] else 0
                facility_analysis[col] = {
                    'available': available,
                    'percentage': (available / total * 100) if total > 0 else 0
                }
        
        return facility_analysis
    
    def identify_high_priority_districts(self, metrics=['enrolment', 'tsr', 'facilities']):
        """Identify districts requiring immediate intervention"""
        if self.df is None:
            return None
        
        priority_scores = pd.DataFrame()

        state_col = None
        district_col = None
        
        for col in ['State', 'state', 'STATE', 'State_Name']:
            if col in self.df.columns:
                state_col = col
                break
        
        for col in ['District', 'district', 'DISTRICT', 'District_Name']:
            if col in self.df.columns:
                district_col = col
                break
        
        if not state_col or not district_col:
            return None
        

        district_data = self.df.groupby([state_col, district_col]).agg({
            col: ['count', 'sum', 'mean'] for col in self.df.select_dtypes(include=[np.number]).columns[:10]
        }).reset_index()
        

        priority_scores['district'] = district_data[district_col]
        priority_scores['state'] = district_data[state_col]
        priority_scores['priority_score'] = 0  
        
        return priority_scores.sort_values('priority_score')
    
    def perform_clustering_analysis(self, n_clusters=5, features=None):
        """Perform clustering to identify similar districts/states"""
        if self.df is None:
            return None
        
  
        if features is None:
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            features = numeric_cols[:20]  
        
   
        X = self.df[features].fillna(0)
    
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
      
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(X_scaled)
        
        self.df['cluster'] = clusters
        
        return {
            'clusters': clusters,
            'cluster_centers': kmeans.cluster_centers_,
            'inertia': kmeans.inertia_
        }
    
    def calculate_equity_indicators(self):
        """Calculate equity indicators (rural-urban, gender, etc.)"""
        if self.df is None:
            return None
        
        equity_metrics = {}

        rural_cols = [col for col in self.df.columns if 'rural' in col.lower()]
        urban_cols = [col for col in self.df.columns if 'urban' in col.lower()]
        
        if rural_cols and urban_cols:
            rural_total = self.df[rural_cols[0]].sum() if len(rural_cols) == 1 else self.df[rural_cols].sum(axis=1).sum()
            urban_total = self.df[urban_cols[0]].sum() if len(urban_cols) == 1 else self.df[urban_cols].sum(axis=1).sum()
            
            equity_metrics['rural_urban_ratio'] = rural_total / (urban_total + 1e-10)
        
        return equity_metrics
    
    def generate_policy_recommendations(self):
        """Generate data-driven policy recommendations"""
        recommendations = []
        
  
        
        return recommendations


if __name__ == "__main__":

    analyzer = EducationPolicyAnalyzer()
  

