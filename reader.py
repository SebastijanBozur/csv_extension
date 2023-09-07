import sys
import csv
import json
import pickle
from pathlib import Path

print(sys.argv)


class Parser:

    def __init__(self):
        self.content = []
        self.source = sys.argv[1]
        self.destination = sys.argv[2]

    def parse(self, changes):
        print(self.content)
        for parameter in changes:
            parameter_list = parameter.split(',')
            new_value = ','.join(parameter_list[2:])
            print(parameter_list[0],parameter_list[1],new_value)
            if len(parameter_list) < 3:
                print("Too many or too few values given, no changes saved")
                continue
            column = int(parameter_list[0])
            row = int(parameter_list[1])
            if row < 0 or row > len(self.content):
                print(f"Row value is less or greater than {len(self.content)}")
                continue
            change = self.content[row]
            if column < 0 or column >= len(change):
                print(f"Column value is less or greater than {len(self.content)}")
                continue
            change[column] = new_value
            print(f"Value changed row({row}):column({column}) in value{new_value}")




class ReaderJson:

    def read(self, filepath):
        with open(filepath) as file:
            read = json.load(file)
            self.content = []
            for row in read:
                self.content.append(row)


class WriterJson:

    def write(self, filepath):
        with open(filepath, 'w') as file:
            file.write(json.dumps(self.content))



class ReaderCSV:

    def read(self, filepath):
        with open(filepath) as file:
            read = csv.reader(file)
            self.content = []
            for row in read:
                self.content.append(row)


class WriterCSV:

    def write(self, filepath):
        with open(filepath, 'w', newline='') as file:
            csv.writer(file).writerows(self.content)


class ReaderPickle:

    def read(self, filepath):
        with open(filepath, 'br') as file:
            read = pickle.load(file)
            self.content = []
            for row in read:
                self.content.append(row)


class WritePickle:

    def write(self, filepath):
        with open(filepath, 'bw') as file:
            file.write(pickle.dumps(self.content))


source_ext = Path(sys.argv[1]).suffix
print(source_ext)
if source_ext == '.csv':
    reader = ReaderCSV
elif source_ext == '.json':
    reader = ReaderJson
elif source_ext == '.pkl':
    reader = ReaderPickle

destination_ext = Path(sys.argv[2]).suffix
print(destination_ext)
if destination_ext == '.csv':
    writer = WriterCSV
elif destination_ext == '.json':
    writer = WriterJson
elif destination_ext == '.pkl':
    writer = WritePickle

class Manager(reader,writer,Parser):
    pass


# def factory(source_path, destination_path):
#     source_class = None
#     destination_class = None
#     source_dictionary = {'.cvs': ReaderCVS, '.json': ReaderJson, '.pkl': ReaderPickle}

parser = Manager()

parser.read(sys.argv[1])
parser.parse(sys.argv[3:])
parser.write(sys.argv[2])