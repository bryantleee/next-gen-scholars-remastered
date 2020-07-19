from math import isnan
from difflib import get_close_matches
import pandas as pd
from dateutil import parser

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

    content: IO stream of a CSV file
    valid_students: list strings of of valid students to compare against
    valid_colleges: list strings of of valid colleges to compare against
    '''
    # Try to transform into dataframe
    try:
        df = pd.read_csv(content)
    except:
        return False, 'There is a fatal CSV formatting error. Please redownload the CSV and try again.'
    
    # validate proper number of rows
    if df.shape[1] != 7:
        return False, \
        'We detected {} column{} in this CSV. Make sure there are only 7 columns, as shown exactly in the picture.'\
            .format(df.shape[1], 's' if df.shape[1] != 1 else '')
    # error_list = [] #TODO: Implement me (need to deal with bad types if implemented)
    valid_statuses = (
        'Accepted',
        'Denied',
        'Waitlisted/Deferred (Withdrew App)',
        'Waitlisted/Deferred (Accepted)',
        'Waitlisted/Deferred (Denied)'
    )
    
    #validate each point as a proper data type
    data_validation = {
        'student name' : [str, valid_students, None],
        'college' : [str, valid_colleges, None],
        'application status' : [str, valid_statuses, None], 
        'gpa' : [(int, float), (0, 10), None],
        'sat2400' : [(int, float), (0, 2400), 10],
        'sat1600' : [(int, float), (0, 1600), 10],
        'act' : [(int, float), (0, 36), 1]
    }
    df.columns=[key for key in data_validation]
    for col in df:
        validation_data = data_validation[col] 
        for i, data_point in enumerate(df[col]):
            if data_point is None:
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
    

def parse_dates(column_of_strings):
    '''
    Parses dates for a list/column of strings. Returns a list of dt objects 
    Will return None if it cannot parse a date
    
    this will allow more fluid types of date inputs rather than using pd.to_datetime
    '''
    dt_objects = []
    for date in column_of_strings:
        try:
            dt_objects.append(parser.parse(date))
        except (ValueError, TypeError):
            # Unable to parse date from string or if is value is not a string
            dt_objects.append(None) 
    return dt_objects


def validate_college_csv(content):
    '''
    Validates college upload CSV.
    
    content: IO stream of a CSV file
    '''
    # Try to transform into dataframe
    try:
        df = pd.read_csv(content)
    except:
        return False, 'There is a fatal CSV formatting error. Please redownload the CSV and try again.'
    
    df_columns = ('College','Description', 'Unweighted GPA', 
               'Regular Deadline (RD)', 'Early Deadline (ED)', 
               'Scholarship Deadline', 'FAFSA Deadline', 
               'Acceptance Announcement Date')
    
    date_cols = ('Regular Deadline (RD)', 'Early Deadline (ED)', 'Scholarship Deadline', 'FAFSA Deadline')
    
    # make sure there are the right amount of columns
    if df.shape[1] != 8:
        return False, \
            'There are {} columns. Please make sure that there are 8 columns, as show exactly in the picture.'.format(df.shape[1])
    
    df.columns = df_columns
    
    # Turn dates into DT Objects
    for date_col in date_cols:
        df[date_col] = parse_dates(df[date_col])
    
    # Validate if GPA data
    for unweighted_gpa in df['Unweighted GPA']:
        try:
            float(unweighted_gpa)
        except ValueError:
            return False, \
                'GPA Value type is not correct. Make sure all numbers in the column are numbers with decimals.'
        
        if not 0 <= unweighted_gpa <= 5:
            return False, \
                '{} is not a valid GPA value.'.format(unweighted_gpa)
        
    return True, df