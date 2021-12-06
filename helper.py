import os


def read_file(filename):
    path = os.path.join(os.getcwd(), 'inputs', filename)
    f = open(path, 'r')
    return f.read()
