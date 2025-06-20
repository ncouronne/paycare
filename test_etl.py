import pytest
import pandas as pd
from io import StringIO
from etl import extract_data, transform_data, load_data

# Test for data extraction
def test_extract_data():
    csv_data = StringIO("employee_id,employee_name,salary\n101,Alice,5000\n102,Bob,6000")
    data = pd.read_csv(csv_data)
    assert data is not None
    assert len(data) == 2

# Test for data transformation
def test_transform_data():
    data = pd.DataFrame({
        'employee_id': [101, 102],
        'employee_name': ['Alice', 'Bob'],
        'salary': [5000, 6000]
    })
    
    transformed_data = transform_data(data)
    assert 'tax' in transformed_data.columns
    assert 'net_salary' in transformed_data.columns
    assert transformed_data['tax'][0] == 500  # 10% of 5000
    assert transformed_data['net_salary'][0] == 4500  # 5000 - 500

# Test for data loading
def test_load_data(tmpdir):
    data = pd.DataFrame({
        'employee_id': [101],
        'employee_name': ['Alice'],
        'salary': [5000],
        'tax': [500],
        'net_salary': [4500]
    })
    
    output_file = tmpdir.join("output_data.csv")
    load_data(data, str(output_file))
    loaded_data = pd.read_csv(output_file)
    
    assert len(loaded_data) == 1
    assert loaded_data['employee_name'][0] == 'Alice'
    assert loaded_data['net_salary'][0] == 4500
