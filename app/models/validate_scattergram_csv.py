import pandas as pd
from difflib import get_close_matches
from math import isnan

def is_in_range(value, valid_ranges_inclusive):
    '''
    Writing my own in range function because in range() is not supported for floats and is not inclusive
    Checks if value is in a range designated by valid_ranges_inclusive

    value: float or integer of value you want to check
    valid_ranges_inclusive: tuple containing the min and the max of valid ranges
    '''
    return valid_ranges_inclusive[0] <= value <= valid_ranges_inclusive[1]


def validate_scattergram_csv(content, valid_students, valid_colleges):
    '''
    Validates data in the scattergram uploading CSV

    content: raw string of a CSV file
    valid_students: list strings of of valid students to compare against
    valid_colleges: list strings of of valid colleges to compare against
    '''
    # Try to transform into dataframe
    try:
        df = pd.read_csv(content)
    except:
        return False, 'There is a fatal CSV formatting error. Please redownload the CSV and try again.'

    # validate proper number of rows
    if df.shape[1] != 9:
        return False, \
        'We detected {} column{} in this CSV. Make sure there are only 9 columns, as shown exactly in the picture.'\
            .format(df.shape[1], 's' if df.shape[1] != 1 else '')
    # error_list = [] #TODO: Implement me (need to deal with bad types if implemented)
    valid_ed_statuses = ('ED', 'RD')

    #validate each point as a proper data type
    data_validation = {
        'student name' : [str, None, None],
        'college' : [str, None, None],
        'ed_status' : [str, valid_ed_statuses, None],
        'gpa' : [(int, float), (0, 10), None],
        'sat2400' : [(int, float), (0, 2400), 10],
        'sat1600' : [(int, float), (0, 1600), 10],
        'act' : [(int, float), (0, 36), 1],
        'fin aid' : [(int, float), (0, 1), None],
        'high school': [str, None, None]
    }
    df.columns=[key for key in data_validation]
    for col in df:
        validation_data = data_validation[col]
        for i, data_point in enumerate(df[col]):
            if data_point is None:
                continue

            if validation_data[1] == None:
                continue

            # Ensure data point is the correct data type
            if not isinstance(data_point, validation_data[0]):
                return False, \
                    'Check over your data again. {} should not be in the {} column'.format(data_point, col)

            # Number-specific validation checks
            if isinstance(data_point, (float, int)) and not isnan(data_point):
                # Ensure int/float data points are in valid ranges
                if not is_in_range(data_point, validation_data[1]):
                    return False, '{} is outside the valid range of {} - {} for the {}'.format(
                        data_point, validation_data[1][0], validation_data[1][1], col)

                # Ensure scores are valid, even within the valid range
                if validation_data[2] is not None and data_point % validation_data[2] != 0:
                    return False, '{} is not a valid {} score'.format(data_point, col)

            # String-specific validation checks
            if isinstance(data_point, str):
                # match closest spelling
                lowered_valid_strings = [valid_str.lower() for valid_str in validation_data[1]]
                closest_matches = get_close_matches(data_point.lower(), lowered_valid_strings, cutoff=0.8, n=1)

                # check if that string is a valid category
                if closest_matches:
                    df.at[i, col] = closest_matches[0].title()
                else:
                    error_message = 'No {} match by the name of {}.'.format(col, data_point)
                    if col == 'college':
                        error_message += 'Be sure to add the college first in the Colleges page.'
                    return False, error_message

    return True, df

if __name__ == '__main__':
    df = pd.DataFrame([
        ['Billy Numerous', 'Cornell University', 'Denied', 1.2, None, 1300, None],
        ['Kanye West', None, None, 3.2, 2400, 0, 32]
    ])
    valid_students = ['Bryant Lee', 'Jimmy Pee', 'Kyle Sayers', 'Billy Numerous', 'Kanye West']
    valid_colleges = ['Cornell University', 'Princeton University', 'Boston University', 'Boston College']

    print(validate_scattergram_csv(df, valid_students, valid_colleges))
