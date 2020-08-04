from .. import db
import re

class EditableHTML(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    editor_name = db.Column(db.String(100), unique=True)
    value = db.Column(db.Text)

    @staticmethod
    def get_editable_html(editor_name):
        editable_html_obj = EditableHTML.query.filter_by(
            editor_name=editor_name).first()

        if editable_html_obj is None:
            editable_html_obj = EditableHTML(editor_name=editor_name, value='')
        return editable_html_obj


def get_state_name_from_abbreviation(state):
    states = {
            # U.S. States and Washington D.C.
            'AK': 'Alaska',
            'AL': 'Alabama',
            'AR': 'Arkansas',
            'AS': 'American Samoa',
            'AZ': 'Arizona',
            'CA': 'California',
            'CO': 'Colorado',
            'CT': 'Connecticut',
            'DC': 'District of Columbia',
            'DE': 'Delaware',
            'FL': 'Florida',
            'GA': 'Georgia',
            'GU': 'Guam',
            'HI': 'Hawaii',
            'IA': 'Iowa',
            'ID': 'Idaho',
            'IL': 'Illinois',
            'IN': 'Indiana',
            'KS': 'Kansas',
            'KY': 'Kentucky',
            'LA': 'Louisiana',
            'MA': 'Massachusetts',
            'MD': 'Maryland',
            'ME': 'Maine',
            'MI': 'Michigan',
            'MN': 'Minnesota',
            'MO': 'Missouri',
            'MP': 'Northern Mariana Islands',
            'MS': 'Mississippi',
            'MT': 'Montana',
            'NA': 'National',
            'NC': 'North Carolina',
            'ND': 'North Dakota',
            'NE': 'Nebraska',
            'NH': 'New Hampshire',
            'NJ': 'New Jersey',
            'NM': 'New Mexico',
            'NV': 'Nevada',
            'NY': 'New York',
            'OH': 'Ohio',
            'OK': 'Oklahoma',
            'OR': 'Oregon',
            'PA': 'Pennsylvania',
            'PR': 'Puerto Rico',
            'RI': 'Rhode Island',
            'SC': 'South Carolina',
            'SD': 'South Dakota',
            'TN': 'Tennessee',
            'TX': 'Texas',
            'UT': 'Utah',
            'VA': 'Virginia',
            'VI': 'Virgin Islands',
            'VT': 'Vermont',
            'WA': 'Washington',
            'WI': 'Wisconsin',
            'WV': 'West Virginia',
            'WY': 'Wyoming',


            # Canada
            'AB': 'Alberta',
            'BC': 'British Columbia',
            'MB': 'Manitoba',
            'NB': 'New Brunswick',
            'NL': 'Newfoundland and Labrador',
            'NT': 'Northwest Territories',
            'NS': 'Nova Scotia',
            'NU': 'Nunavut',
            'ON': 'Ontario',
            'PE': 'Prince Edward Island',
            'QC': 'Quebec',
            'SK': 'Saskatchewan',
            'YT': 'Yukon',


            # Provinces
            'AB': 'Alberta',
            'BC': 'British Columbia',
            'MB': 'Manitoba',
            'NB': 'New Brunswick',
            'NL': 'Newfoundland and Labrador',
            'NS': 'Nova Scotia',
            'ON': 'Ontario',
            'PE': 'Prince Edward Island',
            'QC': 'Quebec',
            'SK': 'Saskatchewan',

            # Territories
            'NT': 'Northwest Territories',
            'NU': 'Nunavut',
            'YT': 'Yukon'
    }
    return states.get(state, '')


# will fix URL in user forms so that they are clickable if http/https not included
# you can always add http because it will get bumped up to https if available, 
# but you can't bump down from https to http
def fix_url(url):
    if url:
        match = re.search('^https?:\/\/', url)
        if not match:
            url = 'http://' + url
        return url


# will parse out the Collegecard ID from either URL or raw id input. 
# if the name of a college is input, it will return empty string.
# will return 0 if it is a name, return 1 if it is a number
def interpret_scorecard_input(form_input):
    inputted_id = re.search('(?:https?:\/\/collegescorecard\.ed\.gov\/school\/\?)?(\d+)', form_input)
    if inputted_id is None:
        return ''
    groups = inputted_id.groups()
    for group in groups:
        if group is not None:
            return group
    return ''

def extract_url_or_name(form_input):
    matches = re.findall('^.*collegescorecard.ed.gov/school/\?(\d+).*$', form_input.strip())
    if matches:
        return int(matches[0]), 'scorecard_id'
    return form_input, 'name'

def get_colors():
    return ('red', 'orange', 'yellow', 'olive', 'green', 'teal', 'blue', 'violet', 'purple', 'pink')


def get_easter_egg_emoji(college_name):
    '''
    college_name: string
        gets emoji for a college, given a college name
        returns string with emoji
    '''
    easter_eggs = {
        'Tufts University' : '🐘',
        'Cornell University' : '🌽',
        'Stanford University' : '🌲',
        'University of Richmond' : '🕷',
        'University of Pennsylvania' : '🖋️',
        'Brown University' : '🐻'
    }
    return easter_eggs.get(college_name)

def calculate_luminescence(r, g, b):
    '''
    - r: int 
        red color between 0 and 255
    - g: int
        green color between 0 and 255
    - b: int
        blue color between 0 and 255
    
    Calculates luminance of a, returns a single float between 0 and 1 that represents luminescence
    
    See this page for more info:
    https://www.w3.org/TR/WCAG20/#contrast-ratiodef
    '''
    colors = (r/255, g/255, b/255)
    final_colors = tuple(color/12.92 if color <= 0.03928 else ((color + 0.055) / 1.055) ** 2.4 for color in colors)
    return 0.2126 * final_colors[0] + 0.7152 * final_colors[1] + 0.0722 * final_colors[2]


def calculate_luminescence_ratio(color1, color2, color_format='hex'):
    '''
    - color1: 
        tuple of (r: int, g: int, b: int) OR
        tuple of (r: int, g: int, b: int, a: int) OR
        str of hex format '#XXXXXX' OR 'XXXXXX'
            represents the first color you want to check 
    - color2: 
        tuple of (r: int, g: int, b: int) OR
        tuple of (r: int, g: int, b: int, a: int) OR
        str of hex format '#XXXXXX' OR 'XXXXXX'
            represents the second color you want to check 
    
    color_format: str of either {'hex', 'rgba', or 'rgb'}
        describes the color format of color1 and color2
        both color1 and color2 should be the same color format
    
    Calculates luminescence ratio between two colors, outputs a float between 0 and 21.
    The higher the number, the better. 
    Ideally should be:
        ≥ 3.0 for large text  
        ≥ 4.5 for everything else
    
    See this page for more info:
    https://www.w3.org/TR/WCAG20/#contrast-ratiodef
    '''
    color_luminescences = []
    for color in (color1, color2):
        if color_format == 'hex':
            color = (lambda x : tuple(int(x.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)))(color)
        elif color_format == 'rgba':
            color = color[-1]
        color_luminescences.append(calculate_luminescence(color[0], color[1], color[2]))
    
    ratio1 = (color_luminescences[0] + 0.05) / (color_luminescences[1] + 0.05)
    ratio2 = (color_luminescences[1] + 0.05) / (color_luminescences[0] + 0.05)
    return max(ratio1, ratio2)