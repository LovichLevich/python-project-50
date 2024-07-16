from gendiff.engine import convert_value_to_string, generate_diff

def test_convert_value_to_string_none():
    assert convert_value_to_string(None) == 'none'

def test_convert_value_to_string_bool_true():
    assert convert_value_to_string(True) == 'true'

def test_convert_value_to_string_bool_false():
    assert convert_value_to_string(False) == 'false'

def setup_files():
    file1_path = 'tests/test_data/file1.json'
    file2_path = 'tests/test_data/file2.json'
    
def test_generate_diff(setup_files):
    file1_path, file2_path = setup_files
    
    expected_diff = """{
  - follow: false
  - proxy: 123.234.53.22
  - timeout: 50
  + timeout: 20
  + verbose: true
}"""
    
    assert generate_diff(file1_path, file2_path) == expected_diff