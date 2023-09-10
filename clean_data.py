# Your code here

import numpy as np
import pandas as pd
import uuid

# Data Cleaning and Formatting¶
# Cleaning Column Names

#change column names to lower case
from pandas import DataFrame

# Define the changes and string operations for each column
changes = {
    'gender': {'female': 'F', 'Male': 'M', 'Femal': 'F', 'm': 'M'},
    'state': {'AZ': 'Arizona', 'Cali': 'California', 'WA': 'Washington'},
    'education': {'Bachelors': 'Bachelor'},
    # Add more columns and their changes as needed
}


def change_col_names_to_lower_case(df: DataFrame) -> DataFrame:
    '''
    This function changes the case of the column names to lowercase.

    Args:
    - df (DataFrame): The input DataFrame.

    Returns:
    - DataFrame: A new DataFrame with lowercase column names.
    '''
    # Create a new DataFrame with lowercase column names
    #df1 = df.copy()
    df.columns = df.columns.str.lower()
    
    return df
# replacing White spaces in column names by _

def replace_white_spaces_in_col_names(df: DataFrame) -> DataFrame:
    '''
    This function white spaces in the column names.

    Args:
    - df (DataFrame): The input DataFrame.

    Returns:
    - DataFrame: A new DataFrame with remove white spaces from column names.
    '''
    # Create a new DataFrame with lowercase column names
    df.columns = df.columns.str.replace(" ","-")
        
    return df

#other changes in data frame and st could be replaced for state

def rename_col_names(df: DataFrame, column_names:dict)-> DataFrame:
    """
    Rename columns in a DataFrame based on a dictionary of column names.

    Args:
    - df (DataFrame): The input DataFrame.
    - column_names (dict): A dictionary mapping old column names to new column names.

    Returns:
    - DataFrame: A new DataFrame with renamed columns.
    """
    # Use the .rename() method with columns parameter
    df=df.rename(columns=column_names)
    return df
# Function to clean columns by mapping values
def clean_column_by_mapping(df):
    """
    Clean columns in the DataFrame by mapping values to new values.

    Args:
    - df (DataFrame): The input DataFrame.
    - changes (dict): A dictionary where keys are column names and values are dictionaries
                      mapping old values to new values for each column.

    Returns:
    - DataFrame: The DataFrame with specified columns cleaned.
    """
    for column, value_mapping in changes.items():
        if column in df.columns:
            df[column] = df[column].replace(value_mapping)
    return df

# Function to clean columns by applying a string operation
def clean_column_by_string_operation(df, string_operations):
    """
    Clean columns in the DataFrame by applying string operations to their values.

    Args:
    - df (DataFrame): The input DataFrame.
    - changes (dict): A dictionary where keys are column names and values are functions
                      to apply to the column values.
    - string_operations (dict): A dictionary where keys are column names and values
                                are string operations to apply to the column values.

    Returns:
    - DataFrame: The DataFrame with specified columns cleaned.
    """
    for column, string_operation in string_operations.items():
        if column in df.columns:
            df[column] = df[column].apply(string_operation)
    return df


def strip_percentage(value):
    return str(value).rstrip('%')

def map_vehicle_class(value):
    return 'Luxury' if value in ['Sports Car', 'Luxury SUV', 'Luxury Car'] else value 
def handle_missing_values(df: DataFrame, numerical_columns1_mean: list, numerical_columns2_median: list, categorical_columns_mode: list) -> DataFrame:
    '''
    Handle missing values in a DataFrame.

    Args:
    - df (DataFrame): The input DataFrame with missing values.
    - numerical_columns1_mean (list): List of numerical columns for which to fill missing values with mean.
    - numerical_columns2_median (list): List of numerical columns for which to fill missing values with median.
    - categorical_columns_mode (list): List of categorical columns for which to fill missing values.

    Returns:
    - DataFrame: The DataFrame with missing values handled.
    '''
    
    # Identify columns with missing values
    null_columns = df.columns[df.isnull().any()]

    # Iterate through the columns with null values and print the count of null values in each
    for column in null_columns:
        null_count = df[column].isnull().sum()
        print(f"Column '{column}' has {null_count} null values.")

    # Fill missing values in the 'id' column with random UUIDs
    df['id'].fillna(uuid.uuid4(), inplace=True)

    # Convert columns to numeric and replace non-numeric values with NaN
    #df[numerical_columns1_mean] = pd.to_numeric(df[numerical_columns1_mean], errors='coerce')
    #df[numerical_columns2_median] = pd.to_numeric(df[numerical_columns2_median], errors='coerce')

    # Fill missing values in numerical columns with their mean or median
    for col in numerical_columns1_mean:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df[col] = df[col].fillna(df[col].mean())
    
    for col in numerical_columns2_median:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df[col] = df[col].fillna(df[col].median())

    # Fill missing values in categorical columns with their mode
    for col in categorical_columns_mode:
        df[col].fillna(df[col].mode()[0], inplace=True)

    # Fill NaN values with zero for numerical columns in numerical_columns1_mean
    df[numerical_columns1_mean] = df[numerical_columns1_mean].fillna(0)
    

    # Convert filled columns to integers using applymap
    #for col in numerical_columns2_median:
    df[numerical_columns1_mean] = df[numerical_columns1_mean].applymap(int)
    df[numerical_columns2_median] = df[numerical_columns2_median].applymap(int)

    # Iterate through the columns with null values again and print the count of null values in each
    null_columns = df.columns[df.isnull().any()]
    for column in null_columns:
        null_count = df[column].isnull().sum()
        print(f"Column '{column}' has {null_count} null values.")

    return df
# Identify duplicate rows
def duplicate_rows(df:DataFrame,subset_columns:list)->DataFrame:
    duplicates = df[df.duplicated()]

# Print the duplicate rows
    print("Duplicate Rows:")
    print(duplicates.count())


# Remove duplicate rows based on the 'id' column
    df_cleaned = df.drop_duplicates(subset=subset_columns)

    duplicates = df_cleaned[df_cleaned.duplicated()]

# Print the duplicate rows
    print("Duplicate Rows:")
    print(duplicates.count())

    df_cleaned.to_csv('cleaned_insurance_data.csv', index=False)
    return df
