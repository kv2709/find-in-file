import os
import datetime
from collections import deque

def prepare_search_str(str_for_search):
    lst_search_byte = []
    lst_search_str = str_for_search.split(' ')
    count_byte_search = len(lst_search_str)
    for i in range(count_byte_search):
        if lst_search_str[i] != '?':
            lst_search_byte.append(int(lst_search_str[i], 16))
        else:
            lst_search_byte.append(500)
    return count_byte_search, lst_search_byte


class FinderBF():
    """Read data file and find in them byte array"""
    def __init__(self, path_to_file, str_for_search):
        self.path_to_file = path_to_file
        self.str_for_search = str_for_search
        self.lst_byte_from_file = []
        self.lst_search_str = []
        self.lst_search_byte = []
        self.lst_position_found = []
        self.file_size = os.path.getsize(self.path_to_file)
        self.time_search_in_file = None
        self.error_reading_file = 'Error reading file'


    def search(self):
        try:
            time_start = datetime.datetime.now()
            fd = open(self.path_to_file, 'rb')
            str_byte_file = fd.read()
            fd.close()
            count_byte_in_file = len(str_byte_file)
            for i in range(count_byte_in_file):
                self.lst_byte_from_file.append(int(str_byte_file[i]))
            count_byte_search, self.lst_search_byte = prepare_search_str(self.str_for_search)
            id_f = 0

            while id_f <= count_byte_in_file - count_byte_search:
                lst_found = []
                for j in range(count_byte_search):
                    if self.lst_search_byte[j] == self.lst_byte_from_file[id_f + j]:
                        lst_found.append(True)
                    else:
                        if self.lst_search_byte[j] == 500:
                            lst_found.append(True)
                        else:
                            lst_found.append(False)
                sum_found = all(lst_found)
                if sum_found:
                    self.lst_position_found.append(id_f)
                id_f += 1
            time_finish = datetime.datetime.now()
            self.time_search_in_file = time_finish - time_start
        except FileNotFoundError:
            return self.error_reading_file

    def result(self):
        return self.lst_position_found
    def time_search(self):
        return self.time_search_in_file


class CombBF():
    """
        Search in file use method riding from this byte to byte
    """
    def __init__(self, path_to_file, str_for_search):
        self.path_to_file = path_to_file
        self.str_for_search = str_for_search
        self.lst_byte_from_file = []
        self.lst_search_str = []
        self.lst_search_byte = []
        self.lst_position_found = []
        self.file_size = os.path.getsize(self.path_to_file)
        self.time_search_in_file = None
        self.error_reading_file = 'Error reading file'

    def search(self):
        try:
            time_start = datetime.datetime.now()
            fd = open(self.path_to_file, 'rb')
            count_byte_in_file = self.file_size
            count_byte_search, self.lst_search_byte = prepare_search_str(self.str_for_search)
            id_f = 0
            queue_on_file = deque()
            while id_f <= count_byte_in_file:
                if id_f < count_byte_search:
                    queue_on_file.append(int(fd.read(1)[0]))
                else:
                    lst_found = []
                    for j in range(count_byte_search):
                        if self.lst_search_byte[j] == queue_on_file[j]:
                            lst_found.append(True)
                        else:
                            if self.lst_search_byte[j] == 500:
                                lst_found.append(True)
                            else:
                                lst_found.append(False)
                    sum_found = all(lst_found)
                    if sum_found:
                        self.lst_position_found.append(id_f - count_byte_search)
                    if id_f == count_byte_in_file:
                        break
                    queue_on_file.popleft()
                    queue_on_file.append(int(fd.read(1)[0]))
                id_f += 1
            fd.close()
            time_finish = datetime.datetime.now()
            self.time_search_in_file = time_finish - time_start
        except FileNotFoundError:
            return self.error_reading_file

    def result(self):
        return self.lst_position_found

    def time_search(self):
        return self.time_search_in_file