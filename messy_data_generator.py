import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import string
import os
import argparse

class AdvancedMessyDataGenerator:
    def __init__(self, sample_df=None):
        """
        Initialize the generator with a sample DataFrame
        """
        if sample_df is None:
            raise ValueError("Please provide a sample DataFrame")
        self.sample_df = sample_df.copy()
        self.column_types = self._analyze_columns()
    
    def _analyze_columns(self):
        """Analyze column types and patterns"""
        column_info = {}
        
        for col in self.sample_df.columns:
            col_data = self.sample_df[col].dropna()
            
            if len(col_data) == 0:
                column_info[col] = {'type': 'mixed', 'samples': []}
                continue
                
            # Determine column type
            if pd.api.types.is_numeric_dtype(col_data):
                column_info[col] = {
                    'type': 'numeric',
                    'min': col_data.min(),
                    'max': col_data.max(),
                    'samples': col_data.tolist()
                }
            elif pd.api.types.is_datetime64_any_dtype(col_data):
                column_info[col] = {
                    'type': 'datetime',
                    'min': col_data.min(),
                    'max': col_data.max(),
                    'samples': col_data.tolist()
                }
            else:
                # String or categorical
                unique_vals = col_data.unique()
                column_info[col] = {
                    'type': 'categorical' if len(unique_vals) < len(col_data) * 0.8 else 'text',
                    'samples': col_data.tolist(),
                    'unique_values': unique_vals.tolist()
                }
        
        return column_info
    
    def generate_messy_data(self, 
                          target_rows=10000,
                          duplicate_rate=0.15,
                          null_rate=0.10,
                          wrong_range_rate=0.08,
                          wrong_timestamp_rate=0.05,
                          text_corruption_rate=0.05):
        """
        Generate messy data with customizable parameters
        """
        print(f"Generating messy dataset with {target_rows} rows...")
        print(f"Original dataset: {len(self.sample_df)} rows, {len(self.sample_df.columns)} columns")
        
        # Step 1: Generate base expanded data
        expanded_data = self._expand_data(target_rows)
        
        # Step 2: Introduce various types of messiness
        messy_data = self._introduce_messiness(
            expanded_data,
            duplicate_rate=duplicate_rate,
            null_rate=null_rate,
            wrong_range_rate=wrong_range_rate,
            wrong_timestamp_rate=wrong_timestamp_rate,
            text_corruption_rate=text_corruption_rate
        )
        
        # Step 3: Shuffle data
        messy_data = messy_data.sample(frac=1).reset_index(drop=True)
        
        print(f"Generated dataset: {len(messy_data)} rows")
        return messy_data
    
    def _expand_data(self, target_rows):
        """Expand the original data by generating similar records"""
        expanded_records = []
        
        for i in range(target_rows):
            new_record = {}
            
            for col, info in self.column_types.items():
                new_record[col] = self._generate_similar_value(col, info)
            
            expanded_records.append(new_record)
        
        return pd.DataFrame(expanded_records)
    
    def _generate_similar_value(self, column, col_info):
        """Generate a value similar to existing values in the column"""
        if len(col_info['samples']) == 0:
            return None
            
        col_type = col_info['type']
        
        if col_type == 'numeric':
            # Generate numeric value within similar range
            if random.random() < 0.7:  # 70% similar to existing
                return random.choice(col_info['samples'])
            else:  # 30% interpolated
                min_val, max_val = col_info['min'], col_info['max']
                return random.uniform(min_val, max_val)
                
        elif col_type == 'datetime':
            # Generate datetime within similar range
            if random.random() < 0.7:
                return random.choice(col_info['samples'])
            else:
                min_date = pd.to_datetime(col_info['min'])
                max_date = pd.to_datetime(col_info['max'])
                random_timestamp = random.uniform(min_date.timestamp(), max_date.timestamp())
                return pd.to_datetime(random_timestamp, unit='s')
                
        elif col_type == 'categorical':
            # Choose from existing categories
            return random.choice(col_info['unique_values'])
            
        elif col_type == 'text':
            # Generate similar text
            sample_text = random.choice(col_info['samples'])
            if random.random() < 0.8:  # 80% return existing
                return sample_text
            else:  # 20% generate variation
                return self._generate_text_variation(sample_text)
        
        return random.choice(col_info['samples'])
    
    def _generate_text_variation(self, original_text):
        """Generate variations of text"""
        if not isinstance(original_text, str) or len(original_text) == 0:
            return original_text
            
        variations = [
            original_text + str(random.randint(1, 999)),
            original_text.replace(' ', '_'),
            original_text + random.choice([' Jr', ' Sr', ' II', ' Inc', ' LLC']),
            ''.join(random.choices(string.ascii_letters, k=len(original_text)))
        ]
        
        return random.choice(variations)
    
    def _introduce_messiness(self, df, **rates):
        """Introduce various types of data quality issues"""
        messy_df = df.copy()
        
        # Add duplicates
        messy_df = self._add_smart_duplicates(messy_df, rates['duplicate_rate'])
        
        # Add null values
        messy_df = self._add_strategic_nulls(messy_df, rates['null_rate'])
        
        # Add wrong ranges
        messy_df = self._add_wrong_ranges(messy_df, rates['wrong_range_rate'])
        
        # Add wrong timestamps
        messy_df = self._add_wrong_timestamps(messy_df, rates['wrong_timestamp_rate'])
        
        # Add text corruption
        messy_df = self._add_text_corruption(messy_df, rates['text_corruption_rate'])
        
        return messy_df
    
    def _add_smart_duplicates(self, df, rate):
        """Add exact and near duplicates"""
        num_duplicates = int(len(df) * rate)
        duplicate_indices = np.random.choice(df.index, size=num_duplicates, replace=True)
        
        duplicates = []
        for idx in duplicate_indices:
            duplicate = df.iloc[idx].copy()
            
            # 30% chance to make it a near duplicate
            if random.random() < 0.3:
                # Modify one random column slightly
                text_cols = [col for col, info in self.column_types.items() 
                           if info['type'] in ['text', 'categorical']]
                if text_cols:
                    col_to_modify = random.choice(text_cols)
                    original_val = duplicate[col_to_modify]
                    if isinstance(original_val, str):
                        modifications = [
                            original_val + ' ',  # trailing space
                            original_val.upper(),
                            original_val.lower(),
                            original_val.replace(' ', ''),
                        ]
                        duplicate[col_to_modify] = random.choice(modifications)
            
            duplicates.append(duplicate)
        
        duplicate_df = pd.DataFrame(duplicates)
        return pd.concat([df, duplicate_df], ignore_index=True)
    
    def _add_strategic_nulls(self, df, rate):
        """Add null values strategically"""
        total_cells = df.shape[0] * df.shape[1]
        num_nulls = int(total_cells * rate)
        
        # Some columns are more likely to have nulls
        null_prone_cols = []
        for col, info in self.column_types.items():
            if info['type'] in ['text', 'categorical']:
                null_prone_cols.extend([col] * 3)  # 3x more likely
            else:
                null_prone_cols.append(col)
        
        for _ in range(num_nulls):
            row_idx = random.randint(0, len(df) - 1)
            col_name = random.choice(null_prone_cols)
            df.at[row_idx, col_name] = None
        
        return df
    
    def _add_wrong_ranges(self, df, rate):
        """Add values outside expected ranges"""
        num_wrong = int(len(df) * rate)
        
        for _ in range(num_wrong):
            row_idx = random.randint(0, len(df) - 1)
            
            # Find numeric columns to corrupt
            numeric_cols = [col for col, info in self.column_types.items() 
                          if info['type'] == 'numeric']
            
            if numeric_cols:
                col = random.choice(numeric_cols)
                col_info = self.column_types[col]
                
                # Generate wrong range values
                wrong_values = [
                    col_info['min'] - abs(col_info['max'] - col_info['min']),  # Too low
                    col_info['max'] + abs(col_info['max'] - col_info['min']),  # Too high
                    -999999,  # Clearly wrong
                    999999,   # Clearly wrong
                    0 if col_info['min'] > 0 else -1  # Edge case
                ]
                
                df.at[row_idx, col] = random.choice(wrong_values)
        
        return df
    
    def _add_wrong_timestamps(self, df, rate):
        """Add invalid timestamps"""
        num_wrong = int(len(df) * rate)
        
        datetime_cols = [col for col, info in self.column_types.items() 
                        if info['type'] == 'datetime']
        
        if not datetime_cols:
            return df
        
        for _ in range(num_wrong):
            row_idx = random.randint(0, len(df) - 1)
            col = random.choice(datetime_cols)
            
            wrong_dates = [
                pd.to_datetime('1900-01-01'),  # Too old
                pd.to_datetime('2100-01-01'),  # Future
                pd.NaT,  # Invalid
                pd.to_datetime('1970-01-01'),  # Epoch
            ]
            
            df.at[row_idx, col] = random.choice(wrong_dates)
        
        return df
    
    def _add_text_corruption(self, df, rate):
        """Add text corruption"""
        num_corrupt = int(len(df) * rate)
        
        text_cols = [col for col, info in self.column_types.items() 
                    if info['type'] in ['text', 'categorical']]
        
        if not text_cols:
            return df
        
        for _ in range(num_corrupt):
            row_idx = random.randint(0, len(df) - 1)
            col = random.choice(text_cols)
            original = df.at[row_idx, col]
            
            if isinstance(original, str) and len(original) > 0:
                corruptions = [
                    original.upper(),
                    original.lower(),
                    original + '???',
                    original.replace(original[0], 'X') if len(original) > 0 else original,
                    original[::-1],  # Reverse
                    original + original,  # Duplicate
                    '',  # Empty
                    ''.join(random.choices(string.ascii_letters + string.digits, k=len(original)))
                ]
                
                df.at[row_idx, col] = random.choice(corruptions)
        
        return df
    
    def analyze_data_quality(self, df):
        """Analyze data quality issues"""
        print("\n" + "="*60)
        print("DATA QUALITY ANALYSIS")
        print("="*60)
        
        print(f"Dataset shape: {df.shape}")
        print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        # Duplicates
        duplicates = df.duplicated().sum()
        print(f"\nExact duplicates: {duplicates} ({duplicates/len(df)*100:.2f}%)")
        
        # Null analysis
        print(f"\nNull values by column:")
        null_summary = df.isnull().sum()
        for col, nulls in null_summary.items():
            if nulls > 0:
                print(f"  {col}: {nulls} ({nulls/len(df)*100:.2f}%)")
        
        # Data type issues
        print(f"\nData type analysis:")
        for col in df.columns:
            dtype = df[col].dtype
            unique_vals = df[col].nunique()
            print(f"  {col}: {dtype}, {unique_vals} unique values")
        
        return {
            'shape': df.shape,
            'duplicates': duplicates,
            'null_counts': null_summary.to_dict(),
            'memory_mb': df.memory_usage(deep=True).sum() / 1024**2
        }

def main():
    parser = argparse.ArgumentParser(description='Generate messy data from clean dataset')
    parser.add_argument('input_file', help='Input CSV file path')
    parser.add_argument('--output', '-o', default='messy_data.csv', help='Output file path')
    parser.add_argument('--rows', '-r', type=int, default=10000, help='Target number of rows')
    parser.add_argument('--duplicates', '-d', type=float, default=0.15, help='Duplicate rate (0-1)')
    parser.add_argument('--nulls', '-n', type=float, default=0.10, help='Null rate (0-1)')
    parser.add_argument('--wrong-ranges', '-w', type=float, default=0.08, help='Wrong range rate (0-1)')
    parser.add_argument('--wrong-timestamps', '-t', type=float, default=0.05, help='Wrong timestamp rate (0-1)')
    parser.add_argument('--text-corruption', '-c', type=float, default=0.05, help='Text corruption rate (0-1)')
    
    args = parser.parse_args()
    
    # Load input data
    try:
        if args.input_file.endswith('.csv'):
            sample_df = pd.read_csv(args.input_file)
        elif args.input_file.endswith('.json'):
            sample_df = pd.read_json(args.input_file)
        else:
            raise ValueError("Unsupported file format. Use CSV or JSON.")
        
        print(f"Loaded {len(sample_df)} rows from {args.input_file}")
        
    except Exception as e:
        print(f"Error loading file: {e}")
        return
    
    # Generate messy data
    generator = AdvancedMessyDataGenerator(sample_df)
    
    messy_data = generator.generate_messy_data(
        target_rows=args.rows,
        duplicate_rate=args.duplicates,
        null_rate=args.nulls,
        wrong_range_rate=args.wrong_ranges,
        wrong_timestamp_rate=args.wrong_timestamps,
        text_corruption_rate=args.text_corruption
    )
    
    # Save results
    messy_data.to_csv(args.output, index=False)
    print(f"\nMessy data saved to: {args.output}")
    
    # Analyze quality
    analysis = generator.analyze_data_quality(messy_data)
    
    # Save analysis
    analysis_file = args.output.replace('.csv', '_analysis.txt')
    with open(analysis_file, 'w') as f:
        f.write("Data Quality Analysis Report\n")
        f.write("="*30 + "\n")
        f.write(f"Original file: {args.input_file}\n")
        f.write(f"Generated file: {args.output}\n")
        f.write(f"Dataset shape: {analysis['shape']}\n")
        f.write(f"Duplicates: {analysis['duplicates']}\n")
        f.write(f"Null counts: {analysis['null_counts']}\n")
        f.write(f"Memory usage: {analysis['memory_mb']:.2f} MB\n")
    
    print(f"Analysis report saved to: {analysis_file}")

if __name__ == "__main__":
    main()