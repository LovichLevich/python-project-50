import pytest # type: ignore
from gendiff.engine import generate_diff
from gendiff.filters.plain import plain
from gendiff.filters.stylish import stylish, conv_string
from gendiff.filters.json import gendiff_json 

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
def expected_diff_stylish():
    with open('tests/fixtures/expected_diff_stylish.txt') as f:
        return f.read().strip()
    
@pytest.fixture
def expected_diff_plain():
    with open('tests/fixtures/expected_diff_plain.txt') as f:
        return f.read().strip()
    
@pytest.fixture
def expected_diff_json():
    with open('tests/fixtures/expected_diff_json.txt') as f:
        return f.read().strip()  

@pytest.mark.parametrize("file1_path, file2_path, expected_diff, formatter", [
    ('file1_json_path', 'file2_json_path', 'expected_diff_json', gendiff_json),
    ('file1_yaml_path', 'file2_yaml_path', 'expected_diff_stylish', stylish),
    ('file1_yaml_path', 'file2_yaml_path', 'expected_diff_plain', plain),
])
def test_generate_diff(file1_path, file2_path, expected_diff, formatter, request):
    file1_path = request.getfixturevalue(file1_path)
    file2_path = request.getfixturevalue(file2_path)
    expected_diff = request.getfixturevalue(expected_diff)
    
    diff_result = generate_diff(file1_path, file2_path, formatter)
    assert diff_result == expected_diff