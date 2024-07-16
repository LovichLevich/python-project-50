import json
from gendiff.engine import convert_value_to_string, generate_diff


def test_convert_value_to_string_none():
    assert convert_value_to_string(None) == 'none'

def test_convert_value_to_string_bool_true():
    assert convert_value_to_string(True) == 'true'

def test_convert_value_to_string_bool_false():
    assert convert_value_to_string(False) == 'false'
    
def test_generate_diff(file1_path, file2_path):
    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
        data1 = json.load(file1)
        data2 = json.load(file2)
    
    expected_diff = """{
  - follow: false
  - proxy: 123.234.53.22
  - timeout: 50
  + timeout: 20
  + verbose: true
}"""
    
    assert generate_diff(file1_path, file2_path) == expected_diff