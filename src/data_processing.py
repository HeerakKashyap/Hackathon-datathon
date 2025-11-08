import pandas as pd
import numpy as np
import os
import zipfile
from pathlib import Path


class UDISEDataProcessor:
    """Process UDISE education datasets"""
    
    def __init__(self, data_dir='data/raw'):
        self.data_dir = Path(data_dir)
        self.processed_dir = Path('data/processed')
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        
    def extract_zip_files(self, zip_path):
        """Extract zip files to a directory"""
        extract_dir = self.data_dir / Path(zip_path).stem
        extract_dir.mkdir(parents=True, exist_ok=True)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        return extract_dir
    
    def load_from_zip(self, zip_path, encoding='utf-8'):
        """Load CSV from zip file"""
        try:
            with zipfile.ZipFile(zip_path, 'r') as z:
                csv_files = [f for f in z.namelist() if f.endswith('.csv')]
                if not csv_files:
                    return None
                
                # Read the first CSV file from zip
                csv_file = csv_files[0]
                try:
                    # Try with utf-8 first
                    with z.open(csv_file) as f:
                        df = pd.read_csv(f, low_memory=False, encoding=encoding)
                        return df
                except UnicodeDecodeError:
                    # Try with latin-1 encoding
                    with z.open(csv_file) as f:
                        df = pd.read_csv(f, low_memory=False, encoding='latin-1')
                        return df
        except Exception as e:
            print(f"Error loading from {zip_path}: {e}")
            return None
    
    def load_enrolment_data(self, year='2024-25', file_num=None):
        """Load enrolment data from CSV files in zip archives"""
        enrolment_zips = []
        
        base_path = self.data_dir / 'UDISE Education Dataset-20251108T185729Z-1-001' / 'UDISE Education Dataset' / f'UDISE {year}'
        
        if file_num:
            pattern = f'enrolment_data_{file_num}_All State_{year}.zip'
            zip_path = base_path / pattern
            if zip_path.exists():
                enrolment_zips.append(zip_path)
        else:
            for num in [1, 2]:
                pattern = f'enrolment_data_{num}_All State_{year}.zip'
                zip_path = base_path / pattern
                if zip_path.exists():
                    enrolment_zips.append(zip_path)
        
        if not enrolment_zips:
            print(f"No enrolment data found for {year}")
            return None
        
        dfs = []
        for zip_path in enrolment_zips:
            print(f"Loading {zip_path.name}...")
            df = self.load_from_zip(zip_path)
            if df is not None:
                print(f"  Loaded {len(df):,} rows, {len(df.columns)} columns")
                dfs.append(df)
        
        if dfs:
            print(f"Combining {len(dfs)} enrolment datasets...")
            combined_df = pd.concat(dfs, ignore_index=True)
            print(f"  Combined dataset: {len(combined_df):,} rows, {len(combined_df.columns)} columns")
            return combined_df
        return None
    
    def load_facility_data(self, year='2024-25'):
        """Load facility/infrastructure data from zip archive"""
        base_path = self.data_dir / 'UDISE Education Dataset-20251108T185729Z-1-001' / 'UDISE Education Dataset' / f'UDISE {year}'
        zip_path = base_path / f'facility_data_All State_{year}.zip'
        
        if zip_path.exists():
            print(f"Loading {zip_path.name}...")
            df = self.load_from_zip(zip_path)
            if df is not None:
                print(f"  Loaded {len(df):,} rows, {len(df.columns)} columns")
            return df
        
        print(f"No facility data found for {year}")
        return None
    
    def load_teacher_data(self, year='2024-25'):
        """Load teacher data from zip archive"""
        base_path = self.data_dir / 'UDISE Education Dataset-20251108T185729Z-1-001' / 'UDISE Education Dataset' / f'UDISE {year}'
        zip_path = base_path / f'teacher_data_All State_{year}.zip'
        
        if zip_path.exists():
            print(f"Loading {zip_path.name}...")
            df = self.load_from_zip(zip_path)
            if df is not None:
                print(f"  Loaded {len(df):,} rows, {len(df.columns)} columns")
            return df
        
        print(f"No teacher data found for {year}")
        return None
    
    def load_profile_data(self, year='2024-25', file_num=None):
        """Load school profile data from zip archives"""
        profile_zips = []
        
        base_path = self.data_dir / 'UDISE Education Dataset-20251108T185729Z-1-001' / 'UDISE Education Dataset' / f'UDISE {year}'
        
        if file_num:
            pattern = f'profile_data_{file_num}_All State_{year}.zip'
            zip_path = base_path / pattern
            if zip_path.exists():
                profile_zips.append(zip_path)
        else:
            for num in [1, 2]:
                pattern = f'profile_data_{num}_All State_{year}.zip'
                zip_path = base_path / pattern
                if zip_path.exists():
                    profile_zips.append(zip_path)
        
        if not profile_zips:
            print(f"No profile data found for {year}")
            return None
        
        dfs = []
        for zip_path in profile_zips:
            print(f"Loading {zip_path.name}...")
            df = self.load_from_zip(zip_path)
            if df is not None:
                print(f"  Loaded {len(df):,} rows, {len(df.columns)} columns")
                dfs.append(df)
        
        if dfs:
            print(f"Combining {len(dfs)} profile datasets...")
            combined_df = pd.concat(dfs, ignore_index=True)
            print(f"  Combined dataset: {len(combined_df):,} rows, {len(combined_df.columns)} columns")
            return combined_df
        return None
    
    def clean_data(self, df):
        """Basic data cleaning operations"""
        if df is None:
            return None
    
        df = df.dropna(how='all')
        df = df.dropna(axis=1, how='all')
     
        numeric_cols = df.select_dtypes(include=[object]).columns
        for col in numeric_cols:
            try:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            except:
                pass
        
        return df
    
    def merge_datasets(self, profile_df, enrolment_df, facility_df, teacher_df, 
                      merge_key='School_Code' or 'DISE_Code' or 'UDISE_Code'):
        """Merge different datasets on common key"""
        merged_df = profile_df.copy()
        
        # Try different possible merge keys
        possible_keys = ['pseudocode', 'School_Code', 'DISE_Code', 'UDISE_Code', 
                        'school_code', 'dise_code', 'udise_code', 'udisecode']
        
        merge_key = None
        for key in possible_keys:
            if key in profile_df.columns:
                merge_key = key
                break
        
        if merge_key is None:
            print("Warning: No common merge key found. Using index merge.")
            return merged_df
        
        if enrolment_df is not None and merge_key in enrolment_df.columns:
            merged_df = merged_df.merge(enrolment_df, on=merge_key, how='left', suffixes=('', '_enrol'))
        
        if facility_df is not None and merge_key in facility_df.columns:
            merged_df = merged_df.merge(facility_df, on=merge_key, how='left', suffixes=('', '_facility'))
        
        if teacher_df is not None and merge_key in teacher_df.columns:
            merged_df = merged_df.merge(teacher_df, on=merge_key, how='left', suffixes=('', '_teacher'))
        
        return merged_df
    
    def process_all_data(self, year='2024-25'):
        """Process all datasets for a given year"""
        print(f"Processing UDISE data for {year}...")
      
        profile_df = self.load_profile_data(year)
        enrolment_df = self.load_enrolment_data(year)
        facility_df = self.load_facility_data(year)
        teacher_df = self.load_teacher_data(year)
       
        profile_df = self.clean_data(profile_df)
        enrolment_df = self.clean_data(enrolment_df)
        facility_df = self.clean_data(facility_df)
        teacher_df = self.clean_data(teacher_df)
     
        if profile_df is not None:
            profile_df.to_csv(self.processed_dir / f'profile_{year}.csv', index=False)
        
        if enrolment_df is not None:
            enrolment_df.to_csv(self.processed_dir / f'enrolment_{year}.csv', index=False)
        
        if facility_df is not None:
            facility_df.to_csv(self.processed_dir / f'facility_{year}.csv', index=False)
        
        if teacher_df is not None:
            teacher_df.to_csv(self.processed_dir / f'teacher_{year}.csv', index=False)
        
    
        if profile_df is not None:
            merged_df = self.merge_datasets(profile_df, enrolment_df, facility_df, teacher_df)
            merged_df.to_csv(self.processed_dir / f'merged_{year}.csv', index=False)
            print(f"Processed and saved merged dataset for {year}")
            return merged_df
        
        return None


if __name__ == "__main__":
    processor = UDISEDataProcessor()
