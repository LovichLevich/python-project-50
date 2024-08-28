import json  # type: ignore
import pytest  # type: ignore
from gendiff.engine import generate_diff


@pytest.mark.parametrize(
    "file1, file2, expected_output_file, format_type",
    [
        ('tests/fixtures/file1.json', 'tests/fixtures/file2.json',
         'tests/fixtures/result_json_1_2.txt', None),
        ('tests/fixtures/file1.yaml', 'tests/fixtures/file2.yaml',
         'tests/fixtures/result_json_1_2.txt', None),
        ('tests/fixtures/file3.json', 'tests/fixtures/file4.json',
         'tests/fixtures/result_json_3_4.txt', None),
        ('tests/fixtures/file3.yaml', 'tests/fixtures/file4.yaml',
         'tests/fixtures/result_json_3_4.txt', None),
        ('tests/fixtures/file3.json', 'tests/fixtures/file4.json',
         'tests/fixtures/result_plain.txt', 'plain'),
        ('tests/fixtures/file3.yaml', 'tests/fixtures/file4.yaml',
         'tests/fixtures/result_plain.txt', 'plain'),
        ('tests/fixtures/file3.json', 'tests/fixtures/file4.json',
         'tests/fixtures/result_json_json.txt', 'json'),
        ('tests/fixtures/file3.yaml', 'tests/fixtures/file4.yaml',
         'tests/fixtures/result_json_json.txt', 'json')
    ]
)
def test_generate_diff(file1, file2, expected_output_file, format_type):
    with open(expected_output_file) as f:
        expected_output = f.read()
    if format_type:
        different = generate_diff(file1, file2, format_type)
    else:
        different = generate_diff(file1, file2)
    assert isinstance(different, str)
    if format_type == 'json':
        different_json = json.loads(different)
        expected_json = json.loads(expected_output)
        assert different_json == expected_json
    else:
        assert different == expected_output
