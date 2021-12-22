def read_file(file_name):
    file = open(file_name, 'r')
    data = file.read()
    file.close()
    return data

def write_file(file_name, write_data):
    file = open(file_name, 'w')
    file.write(write_data)
    file.close()

def append_file(file_name, write_data):
    file = open(file_name, 'a')
    file.write(write_data)
    file.close()

def create_file(file_name):
    file = open(file_name, 'x')
    file.close()