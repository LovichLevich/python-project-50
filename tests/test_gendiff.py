from gendiff.engine import generate_diff
import pytest # type: ignore




@pytest.mark.parametrize("file1,file2", [
    ('tests/fixtures/file1.json', 'tests/fixtures/file2.json'),
    ('tests/fixtures/file1.yaml', 'tests/fixtures/file2.yaml')
])
def test_generate_diff(file1, file2):
    expected_output = open('tests/fixtures/result_json_1_2.txt').read()
    different = generate_diff(file1, file2)
    assert type(different) == str
    assert different == expected_output


@pytest.mark.parametrize("file1,file2", [
    ('tests/fixtures/file3.json', 'tests/fixtures/file4.json'),
    ('tests/fixtures/file3.yaml', 'tests/fixtures/file4.yaml')
])
def test_generate_diff_rec(file1, file2):
    expected_output = open('tests/fixtures/result_json_3_4.txt').read()
    different = generate_diff(file1, file2)
    assert type(different) == str
    assert different == expected_output


@pytest.mark.parametrize("file1,file2", [
    ('tests/fixtures/file3.json', 'tests/fixtures/file4.json'),
    ('tests/fixtures/file3.yaml', 'tests/fixtures/file4.yaml')
])
def test_generate_diff_plain(file1, file2):
    expected_output = open('tests/fixtures/result_plain.txt').read()
    different = generate_diff(file1, file2, 'plain')
    assert type(different) == str
    assert generate_diff('tests/fixtures/file3.yaml', 'tests/fixtures/file4.yaml', 'plain') == expected_output

