import pytest  # type: ignore
from gendiff.engine import generate_diff


@pytest.mark.parametrize(
    "file1, file2, expected_output_file, format_type",
    [
        ('tests/fixtures/file1.json', 'tests/fixtures/file2.json',
         'tests/fixtures/result_json_1_2.txt', 'stylish'),
        ('tests/fixtures/file1.yaml', 'tests/fixtures/file2.yaml',
         'tests/fixtures/result_json_1_2.txt', 'stylish'),
        ('tests/fixtures/file3.json', 'tests/fixtures/file4.json',
         'tests/fixtures/result_json_3_4.txt', 'stylish'),
        ('tests/fixtures/file3.yaml', 'tests/fixtures/file4.yaml',
         'tests/fixtures/result_json_3_4.txt', 'stylish'),
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
        different = generate_diff(file1, file2, format_type)
        assert isinstance(different, str)
        assert different == f.read()
