import pytest
import json
import yaml
from gendiff.engine import conv_string, generate_diff


@pytest.mark.parametrize("input, expected", [
    (None, "null"),
    (True, "true"),
    (False, "false"),
])
def test_convert_value_to_string(input, expected):
    assert conv_string(input) == expected
    
@pytest.fixture
def file1_json_path():
    return 'tests/fixtures/file1.json'

@pytest.fixture
def file2_json_path():
    return 'tests/fixtures/file2.json'

@pytest.fixture
def file1_yaml_path():
    return 'tests/fixtures/file1.yaml'

@pytest.fixture
def file2_yaml_path():
    return 'tests/fixtures/file2.yaml'

@pytest.fixture
def expected_diff():
    with open('tests/fixtures/expected_diff.txt') as f:
        return f.read().strip()

@pytest.mark.parametrize("file1_path, file2_path", [
    ('file1_json_path', 'file2_json_path'),
    ('file1_yaml_path', 'file2_yaml_path')
])
def test_generate_diff(file1_path, file2_path, expected_diff, request):
    file1_path = request.getfixturevalue(file1_path)
    file2_path = request.getfixturevalue(file2_path)
    diff_result = generate_diff(file1_path, file2_path)
    assert diff_result == expected_diff
