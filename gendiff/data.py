from os.path import splitext


def data_form(file_path):
    file = ('yaml', 'yml', 'json')
    extension = splitext(file_path)[1][1:]
    if extension in file:
        with open(file_path) as f:
            data = f.read()
            return data, extension
    else:
        raise Exception('Error! Wrong output format')