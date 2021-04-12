import pprint
import re
from datetime import datetime


def read(filename, user_encoding=None, correct_row=False, empty_value=''):
    """
    :param correct_row: if True then a row can be complemented or reduced to a number of headings
    :param filename: a string defining a name of the file in filesystem
    :param user_encoding: a string defining encoding
    :param empty_value: if there is different number of elements in the raw-list then it is complemented with this value
    :return:
    a list of elements, where every element is a list itself containing all the values from the csv line
    the first element in the list contains headings
    """
    if user_encoding is None:
        user_encoding = 'utf-8-sig'
    fields_number = 0
    with open(filename, encoding=user_encoding) as f:
        output_list = []
        # I use generators for memory efficiency
        lines = (line for line in f)
        line = (i.replace('\n', '').replace('\r', '').split(',') for i in lines)
        # # It is a first line
        headings = [x.strip('"') for x in next(line)]
        # Define number of fields
        fields_number = len(headings)
        output_list.append(headings)
        for entry in line:
            for i_2, value in enumerate(entry):
                entry[i_2] = cleanse_and_convert_value(value)
            if correct_row:
                diff = fields_number - len(entry)
                if diff > 0:
                    complement_row(entry, diff, empty_value)
                elif diff < 0:
                    reduce_row(entry, -diff)

            output_list.append(entry)
    return output_list


def complement_row(list_of_values, diff, empty_value):
    for i in range(diff):
        list_of_values.append(empty_value)


def reduce_row(list_of_values, diff):
    for i in range(diff):
        list_of_values.pop()


def cleanse_and_convert_value(value):
    """
    :param value: a string
    :return: a value with correspondent type int, float, string or datetime
    """
    # remove spaces
    clean_value = value.strip()
    # Check match integer
    match = re.fullmatch('^[-+]?[0-9]+$', clean_value)
    if match:
        return int(value)
    # Match float
    match = re.fullmatch('^[-+]?[0-9]+[.][0-9]+$', clean_value)
    if match:
        return float(value)
    # Check quotes at the beginning and at the end
    match = re.fullmatch('^\".*\"$', clean_value)
    if match:
        clean_value = clean_value[1:-1]
    # check if this field is in ISO 8601 format
    match = re.fullmatch('^([0-9]{2,4})-([0-1][0-9])-([0-3][0-9])(?:( [0-2][0-9]):([0-5][0-9]):([0-5][0-9]))?$',
                         clean_value)
    if match:
        return datetime.strptime(clean_value, '%Y-%m-%d %H:%M:%S')
    # Boolean
    if clean_value == 'True':
        return True
    if clean_value == 'False':
        return False

    return clean_value


if __name__ == '__main__':
    test_read = read('barometer-1617.csv', )
    pprint.pprint(test_read)



