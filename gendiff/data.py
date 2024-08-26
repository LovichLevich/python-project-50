from os.path import splitext
from gendiff.constants import ERROR_MESSAGE, EXTENSION_INDEX, \
    SLICE_START_INDEX, SUPPORTED_EXTENSIONS


def data_form(file_path):
    file = SUPPORTED_EXTENSIONS
    extension = splitext(file_path)[EXTENSION_INDEX][SLICE_START_INDEX:]
    if extension in file:
        with open(file_path) as f:
            data = f.read()
            return data, extension
    else:
        raise Exception(ERROR_MESSAGE)
