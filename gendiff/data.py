from os.path import splitext

SUPPORTED_EXTENSIONS = ('yaml', 'yml', 'json')
ERROR_MESSAGE = 'Error! Wrong output format'
EXTENSION_INDEX = 1
SLICE_START_INDEX = 1


def read_file_data(file_path):
    file = SUPPORTED_EXTENSIONS
    extension = splitext(file_path)[EXTENSION_INDEX][SLICE_START_INDEX:]
    if extension in file:
        with open(file_path) as f:
            data = f.read()
            return data, extension
    else:
        raise Exception(ERROR_MESSAGE)
