from . import ScattergramData
from .. import db

import os
import random
from datetime import datetime
import urllib.request, json
import requests
from requests.exceptions import HTTPError
from requests.auth import HTTPBasicAuth
from difflib import get_close_matches

# import plotly.tools as tools
# import plotly.plotly as py
# import plotly.graph_objs as go

# PLOTLY_USERNAME = os.environ.get('PLOTLY_USERNAME')
# PLOTLY_API_KEY = os.environ.get('PLOTLY_API_KEY')

# py.sign_in(PLOTLY_USERNAME, PLOTLY_API_KEY)

# auth = HTTPBasicAuth(PLOTLY_USERNAME, PLOTLY_API_KEY)
# headers = {'Plotly-Client-Platform': 'python'}


class College(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scorecard_id=db.Column(db.Integer,index=True)
    name = db.Column(db.String, index=True)
    institution_type = db.Column(db.String, index=True) #private, public, proprietary
    description = db.Column(db.String, index=True)
    cost_of_attendance = db.Column(db.Integer, index=True)
    image = db.Column(db.String, index=True)
    regular_deadline = db.Column(db.Date, index=True)
    admission_rate = db.Column(db.Float, index=True)
    early_deadline = db.Column(db.Date, index=True)
    fafsa_deadline = db.Column(db.Date, index=True)
    scholarship_deadline = db.Column(db.Date, index=True)
    acceptance_deadline = db.Column(db.String, index=True)
    plot_SAT2400 = db.Column(db.String)
    plot_SAT1600 = db.Column(db.String)
    plot_ACT = db.Column(db.String)

    median_debt_income_0_30000 = db.Column(db.Integer, index=True)
    median_debt_income_30001_75000 = db.Column(db.Integer, index=True)
    median_debt_income_75001_plus = db.Column(db.Integer, index=True)
    median_debt_first_gen = db.Column(db.Integer, index=True)
    median_debt_non_first_gen = db.Column(db.Integer, index=True)

    net_price_0_30000 = db.Column(db.Integer, index=True)
    net_price_30001_48000 = db.Column(db.Integer, index=True)
    net_price_48001_75000 = db.Column(db.Integer, index=True)
    net_price_75001_110000 = db.Column(db.Integer, index=True)
    net_price_110001_plus = db.Column(db.Integer, index=True)

    image = db.Column(db.String, index=True)
    is_hispanic_serving = db.Column(db.Integer, index=True)
    school_url = db.Column(db.String, index=True)
    price_calculator_url = db.Column(db.String, index=True)
    school_size = db.Column(db.Integer, index=True)
    school_city = db.Column(db.String, index=True)
    school_state = db.Column(db.String, index=True)
    tuition_in_state = db.Column(db.Float, index=True)
    tuition_out_of_state = db.Column(db.Float, index=True)
    cost_of_attendance_in_state = db.Column(db.Float, index=True)
    cost_of_attendance_out_of_state = db.Column(db.Float, index=True)
    room_and_board = db.Column(db.Float, index=True)
    gpa_unweighted_average_overall = db.Column(db.Float, index=True)
    sat_score_average_overall = db.Column(db.Float, index=True)
    act_score_average_overall = db.Column(db.Float, index=True)
    first_generation_percentage = db.Column(db.Float, index=True)
    year_data_collected = db.Column(db.String, index=True)
    race_white = db.Column(db.Float, index=True)
    race_black = db.Column(db.Float, index=True)
    race_hispanic = db.Column(db.Float, index=True)
    race_asian = db.Column(db.Float, index=True)
    race_american_indian = db.Column(db.Float, index=True)
    race_native_hawaiian = db.Column(db.Float, index=True)
    race_international = db.Column(db.Float, index=True)

    school_color1 = db.Column(db.String, index=True)
    school_color2 = db.Column(db.String, index=True)
    school_color3 = db.Column(db.String, index=True)
    school_color4 = db.Column(db.String, index=True)
    
    # TODO: Add college dates

    # def update_plots(self):
    #     if (self.plot_SAT2400):
    #         plot_num = self.plot_SAT2400[1 + self.plot_SAT2400.rfind('/')]
    #         requests.post('https://api.plot.ly/v2/files/' +
    #                       PLOTLY_USERNAME + ':' + plot_num + '/trash', auth=auth, headers=headers)
    #         requests.delete('https://api.plot.ly/v2/files/' + username + ':' + plot_num +
    #                         '/permanent_delete', auth=auth, headers=headers)
    #     if (self.plot_SAT1600):
    #         plot_num = self.plot_SAT1600[1 + self.plot_SAT1600.rfind('/')]
    #         requests.post('https://api.plot.ly/v2/files/' +
    #                       PLOTLY_USERNAME + ':' + plot_num + '/trash', auth=auth, headers=headers)
    #         requests.delete('https://api.plot.ly/v2/files/' + username + ':' + plot_num +
    #                         '/permanent_delete', auth=auth, headers=headers)
    #     if (self.plot_ACT):
    #         plot_num = self.plot_ACT[1 + self.plot_ACT.rfind('/')]
    #         requests.post('https://api.plot.ly/v2/files/' +
    #                       PLOTLY_USERNAME + ':' + plot_num + '/trash', auth=auth, headers=headers)
    #         requests.delete('https://api.plot.ly/v2/files/' + username + ':' + plot_num +
    #                         '/permanent_delete', auth=auth, headers=headers)

    #     data = ScattergramData.query.filter_by(college=self.name).all()

    #     college_filename = self.name.replace(' ', '-').lower()

    #     # GPA vs. SAT [2400]
    #     SAT2400_Accepted = []
    #     GPA_SAT2400_Accepted = []
    #     SAT2400_Denied = []
    #     GPA_SAT2400_Denied = []
    #     SAT2400_Waitlisted1 = []
    #     GPA_SAT2400_Waitlisted1 = []
    #     SAT2400_Waitlisted2 = []
    #     GPA_SAT2400_Waitlisted2 = []
    #     SAT2400_Waitlisted3 = []
    #     GPA_SAT2400_Waitlisted3 = []

    #     # GPA vs. SAT [1600]
    #     SAT1600_Accepted = []
    #     GPA_SAT1600_Accepted = []
    #     SAT1600_Denied = []
    #     GPA_SAT1600_Denied = []
    #     SAT1600_Waitlisted1 = []
    #     GPA_SAT1600_Waitlisted1 = []
    #     SAT1600_Waitlisted2 = []
    #     GPA_SAT1600_Waitlisted2 = []
    #     SAT1600_Waitlisted3 = []
    #     GPA_SAT1600_Waitlisted3 = []

    #     # GPA vs. ACT
    #     ACT_Accepted = []
    #     GPA_ACT_Accepted = []
    #     ACT_Denied = []
    #     GPA_ACT_Denied = []
    #     ACT_Waitlisted1 = []
    #     GPA_ACT_Waitlisted1 = []
    #     ACT_Waitlisted2 = []
    #     GPA_ACT_Waitlisted2 = []
    #     ACT_Waitlisted3 = []
    #     GPA_ACT_Waitlisted3 = []

    #     for i in range(len(data)):
    #         if(data[i].SAT2400):
    #             if(data[i].status == 'Accepted'):
    #                 SAT2400_Accepted.append(int(data[i].SAT2400))
    #                 GPA_SAT2400_Accepted.append(data[i].GPA)
    #             elif(data[i].status == 'Denied'):
    #                 SAT2400_Denied.append(int(data[i].SAT2400))
    #                 GPA_SAT2400_Denied.append(data[i].GPA)
    #             elif(data[i].status == 'Waitlisted/Deferred (Accepted)'):
    #                 SAT2400_Waitlisted1.append(int(data[i].SAT2400))
    #                 GPA_SAT2400_Waitlisted1.append(data[i].GPA)
    #             elif(data[i].status == 'Waitlisted/Deferred (Denied)'):
    #                 SAT2400_Waitlisted2.append(int(data[i].SAT2400))
    #                 GPA_SAT2400_Waitlisted2.append(data[i].GPA)
    #             if(data[i].status == 'Waitlisted/Deferred (Withdrew App)'):
    #                 SAT2400_Waitlisted3.append(int(data[i].SAT2400))
    #                 GPA_SAT2400_Waitlisted3.append(data[i].GPA)

    #         if(data[i].SAT1600):
    #             if(data[i].status == 'Accepted'):
    #                 SAT1600_Accepted.append(int(data[i].SAT1600))
    #                 GPA_SAT1600_Accepted.append(data[i].GPA)
    #             elif(data[i].status == 'Denied'):
    #                 SAT1600_Denied.append(int(data[i].SAT1600))
    #                 GPA_SAT1600_Denied.append(data[i].GPA)
    #             elif(data[i].status == 'Waitlisted/Deferred (Accepted)'):
    #                 SAT1600_Waitlisted1.append(int(data[i].SAT1600))
    #                 GPA_SAT1600_Waitlisted1.append(data[i].GPA)
    #             elif(data[i].status == 'Waitlisted/Deferred (Denied)'):
    #                 SAT1600_Waitlisted2.append(int(data[i].SAT1600))
    #                 GPA_SAT1600_Waitlisted2.append(data[i].GPA)
    #             if(data[i].status == 'Waitlisted/Deferred (Withdrew App)'):
    #                 SAT1600_Waitlisted3.append(int(data[i].SAT1600))
    #                 GPA_SAT1600_Waitlisted3.append(data[i].GPA)

    #         if(data[i].ACT):
    #             if(data[i].status == 'Accepted'):
    #                 ACT_Accepted.append(int(data[i].ACT))
    #                 GPA_ACT_Accepted.append(data[i].GPA)
    #             elif(data[i].status == 'Denied'):
    #                 ACT_Denied.append(int(data[i].ACT))
    #                 GPA_ACT_Denied.append(data[i].GPA)
    #             elif(data[i].status == 'Waitlisted/Deferred (Accepted)'):
    #                 ACT_Waitlisted1.append(int(data[i].ACT))
    #                 GPA_ACT_Waitlisted1.append(data[i].GPA)
    #             elif(data[i].status == 'Waitlisted/Deferred (Denied)'):
    #                 ACT_Waitlisted2.append(int(data[i].ACT))
    #                 GPA_ACT_Waitlisted2.append(data[i].GPA)
    #             if(data[i].status == 'Waitlisted/Deferred (Withdrew App)'):
    #                 ACT_Waitlisted3.append(int(data[i].ACT))
    #                 GPA_ACT_Waitlisted3.append(data[i].GPA)

    #     # Create a trace
    #     trace0 = go.Scatter(
    #         x=SAT2400_Accepted,
    #         y=GPA_SAT2400_Accepted,
    #         mode='markers',
    #         name="Accepted"
    #     )

    #     trace1 = go.Scatter(
    #         x=SAT2400_Denied,
    #         y=GPA_SAT2400_Denied,
    #         mode='markers',
    #         name="Denied"
    #     )

    #     trace2 = go.Scatter(
    #         x=SAT2400_Waitlisted1,
    #         y=GPA_SAT2400_Waitlisted1,
    #         mode='markers',
    #         name="Waitlisted/Deferred (Accepted)"
    #     )

    #     trace3 = go.Scatter(
    #         x=SAT2400_Waitlisted2,
    #         y=GPA_SAT2400_Waitlisted2,
    #         mode='markers',
    #         name="Waitlisted/Deferred (Denied)"
    #     )

    #     trace4 = go.Scatter(
    #         x=SAT2400_Waitlisted3,
    #         y=GPA_SAT2400_Waitlisted3,
    #         mode='markers',
    #         name="Waitlisted/Deferred (Withdrew App)"
    #     )

    #     layout1 = go.Layout(
    #         title='{}: SAT [2400] vs. GPA'.format(self.name),
    #         xaxis=dict(
    #             title='SAT [2400]'
    #         ),
    #         yaxis=dict(
    #             title='GPA',
    #         )
    #     )

    #     fig1 = go.Figure(data=[trace0, trace1, trace2,
    #                            trace3, trace4], layout=layout1)
    #     self.plot_SAT2400 = py.plot(
    #         fig1, filename=college_filename + '-sat2400', auto_open=False)

    #     # Create a trace
    #     trace5 = go.Scatter(
    #         x=SAT1600_Accepted,
    #         y=GPA_SAT1600_Accepted,
    #         mode='markers',
    #         name="Accepted"
    #     )

    #     trace6 = go.Scatter(
    #         x=SAT1600_Denied,
    #         y=GPA_SAT1600_Denied,
    #         mode='markers',
    #         name="Denied"
    #     )

    #     trace7 = go.Scatter(
    #         x=SAT1600_Waitlisted1,
    #         y=GPA_SAT1600_Waitlisted1,
    #         mode='markers',
    #         name="Waitlisted/Deferred (Accepted)"
    #     )

    #     trace8 = go.Scatter(
    #         x=SAT1600_Waitlisted2,
    #         y=GPA_SAT1600_Waitlisted2,
    #         mode='markers',
    #         name="Waitlisted/Deferred (Denied)"
    #     )

    #     trace9 = go.Scatter(
    #         x=SAT1600_Waitlisted3,
    #         y=GPA_SAT1600_Waitlisted3,
    #         mode='markers',
    #         name="Waitlisted/Deferred (Withdrew App)"
    #     )

    #     layout2 = go.Layout(
    #         title='{}: SAT [1600] vs. GPA'.format(self.name),
    #         xaxis=dict(
    #             title='SAT1600'
    #         ),
    #         yaxis=dict(
    #             title='GPA',
    #         )
    #     )

    #     fig2 = go.Figure(data=[trace5, trace6, trace7,
    #                            trace8, trace9], layout=layout2)
    #     self.plot_SAT1600 = py.plot(
    #         fig2, filename=college_filename + '-sat1600', auto_open=False)

    #     # Create a trace
    #     trace10 = go.Scatter(
    #         x=ACT_Accepted,
    #         y=GPA_ACT_Accepted,
    #         mode='markers',
    #         name="Accepted"
    #     )

    #     trace11 = go.Scatter(
    #         x=ACT_Denied,
    #         y=GPA_ACT_Denied,
    #         mode='markers',
    #         name="Denied"
    #     )

    #     trace12 = go.Scatter(
    #         x=ACT_Waitlisted1,
    #         y=GPA_ACT_Waitlisted1,
    #         mode='markers',
    #         name="Waitlisted/Deferred (Accepted)"
    #     )

    #     trace13 = go.Scatter(
    #         x=ACT_Waitlisted2,
    #         y=GPA_ACT_Waitlisted2,
    #         mode='markers',
    #         name="Waitlisted/Deferred (Denied)"
    #     )

    #     trace14 = go.Scatter(
    #         x=ACT_Waitlisted3,
    #         y=GPA_ACT_Waitlisted3,
    #         mode='markers',
    #         name="Waitlisted/Deferred (Withdrew App)"
    #     )

    #     layout3 = go.Layout(
    #         title='{}: ACT vs. GPA'.format(self.name),
    #         xaxis=dict(
    #             title='ACT'
    #         ),
    #         yaxis=dict(
    #             title='GPA',
    #         )
    #     )

    #     fig3 = go.Figure(data=[trace10, trace11, trace12,
    #                            trace13, trace14], layout=layout3)
    #     self.plot_ACT = py.plot(
    #         fig3, filename=college_filename + '-act', auto_open=False)

    @staticmethod
    def get_college_by_name(name):
        return College.query.filter_by(name=name).first()

    @staticmethod
    def search_college_scorecard(college):
        ''' This method uses the College Scorecard Data API to retrieve a dictionary
        of information about colleges that match with our query name
        @param name: name of the college we need to look up
        @return a dictionary of information about colleges that match with our query'''


        if college.scorecard_id:
            nameNewFormat='id=' + str(college.scorecard_id)

        else:
            name = 'school.name=' + college.name
            nameNewFormat = name.replace(' ', '%20')

        try:
            data = None
            year='latest'
            urlStr = '' .join(['https://api.data.gov/ed/collegescorecard/v1/schools.json?',
                nameNewFormat,
                '&_fields=school.name,id,school.city,school.state,school.school_url,school.price_calculator_url,',
                'school.minority_serving.hispanic,school.ownership_peps,',
                year, '.admissions.admission_rate.overall,',
                year, '.student.size,',
                year, '.cost.attendance.academic_year,',
                year, '.cost.tuition.in_state,',
                year, '.cost.tuition.out_of_state,',

                #aid/debt
                year, '.aid.median_debt.income.0_30000,',
                year, '.aid.median_debt.income.30001_75000,',
                year, '.aid.median_debt.income.greater_than_75000,',
                year, '.aid.median_debt.non_first_generation_students,',
                year, '.aid.median_debt.first_generation_students,',

                #costs
                year, '.cost.net_price.public.by_income_level.0-30000,',
                year, '.cost.net_price.public.by_income_level.30001-48000,',
                year, '.cost.net_price.public.by_income_level.48001-75000,',
                year, '.cost.net_price.public.by_income_level.75001-110000,',
                year, '.cost.net_price.public.by_income_level.110001-plus,',
                year, '.cost.net_price.private.by_income_level.0-30000,',
                year, '.cost.net_price.private.by_income_level.30001-48000,',
                year, '.cost.net_price.private.by_income_level.48001-75000,',
                year, '.cost.net_price.private.by_income_level.75001-110000,',
                year, '.cost.net_price.private.by_income_level.110001-plus,',

                year, '.admissions.act_scores.midpoint.cumulative,',
                year, '.student.share_firstgeneration,',
                year, '.admissions.sat_scores.average.overall,',
                year, '.student.demographics.race_ethnicity.white,',
                year, '.student.demographics.race_ethnicity.black,',
                year, '.student.demographics.race_ethnicity.hispanic,',
                year, '.student.demographics.race_ethnicity.asian,',
                year, '.student.demographics.race_ethnicity.aian,',
                year, '.student.demographics.race_ethnicity.nhpi,',
                year, '.student.demographics.race_ethnicity.non_resident_alien',
                '&api_key=jjHzFLWEyba3YYtWiv7jaQN8kGSkMuf55A9sRsxl'])

            r = requests.get(urlStr)
            r.raise_for_status()
            data = r.json()
        except HTTPError:
            print(r.status_code)
            print(urlStr)
            print('could not find college scorecard data for', college.name)
            print('type:', type(college.name), '\n')


        else:
            college.year_data_collected = year

        return(data)

    @staticmethod
    def retrieve_college_info(college, change_name=False):
        ''' This method takes in a College, attempts to find the college that best matches
        with our query, and fill in the variables of the college accordingly.
        Always called after college.name has been initialized
        @param name: name of the college we need to look up
        @return a dictionary of information about the college'''
        if(college.name == ''):
            return
        data = College.search_college_scorecard(college)

        if data is None:
            college.scorecard_id=None
            return False

        # If there are some colleges that match with the query
        if(len(data['results']) > 0):
            # Default to the first search result returned
            result = data['results'][0]
            firstFoundIdx = float("inf")
            # Prioritize colleges whose name contain the query name, and of those who do, prioritize
            # those wherein the query name appears earlier in the college's name
            for r in data['results']:
                idx = r['school.name'].find(college.name)
                if idx != -1:
                    if(firstFoundIdx > idx):
                        firstFoundIdx = idx
                        result = r
            y = college.year_data_collected

            if change_name and result['school.name']:
                college.name = result['school.name']

            if result[y + '.admissions.admission_rate.overall'] is not None:
                college.admission_rate = round(result[y + '.admissions.admission_rate.overall']*100,2)
            if result['school.school_url'] is not None:
                college.school_url = result['school.school_url']
            if result['school.price_calculator_url'] is not None:
                college.price_calculator_url = result['school.price_calculator_url']
            if result['id'] is not None:
                college.scorecard_id = result['id']
            if result['school.ownership_peps'] is not None:
                ownership_values = { 1 : 'public', 2 : 'private', 3 : 'proprietary'}
                college.institution_type = ownership_values.get(result['school.ownership_peps'])
            if result[y+'.aid.median_debt.income.0_30000'] is not None:
                college.median_debt_income_0_30000 = result[y+'.aid.median_debt.income.0_30000']
            if result[y+'.aid.median_debt.income.30001_75000'] is not None:
                college.median_debt_income_30001_75000 = result[y+'.aid.median_debt.income.30001_75000']
            if result[y+'.aid.median_debt.income.greater_than_75000'] is not None:
                college.median_debt_income_75001_plus = result[y+'.aid.median_debt.income.greater_than_75000']
            if result[y+'.aid.median_debt.first_generation_students'] is not None:
                college.median_debt_first_gen = result[y+'.aid.median_debt.first_generation_students']
            if result[y+'.aid.median_debt.non_first_generation_students'] is not None:
                college.median_debt_non_first_gen = result[y+'.aid.median_debt.non_first_generation_students']
            if result[y + '.student.size'] is not None:
                college.school_size = result[y + '.student.size']
            if result['school.city'] is not None:
                college.school_city = result['school.city']
            if result['school.state'] is not None:
                college.school_state = result['school.state']
            if result['school.minority_serving.hispanic'] is not None:
                college.is_hispanic_serving = result['school.minority_serving.hispanic']
            if result[y + '.cost.tuition.in_state'] is not None:
                college.tuition_in_state = result[y + '.cost.tuition.in_state']
            if result[y + '.cost.tuition.out_of_state'] is not None:
                college.tuition_out_of_state = result[y + '.cost.tuition.out_of_state']
            if result[y + '.cost.attendance.academic_year'] is not None:
                college.cost_of_attendance_in_state = result[y + '.cost.attendance.academic_year']
            if result[y + '.cost.attendance.academic_year'] is not None and result[y + '.cost.tuition.in_state'] is not None:
                college.room_and_board = result[y + '.cost.attendance.academic_year'] - result[y + '.cost.tuition.in_state']
            if result[y + '.cost.tuition.out_of_state'] is not None:
                college.cost_of_attendance_out_of_state = college.tuition_out_of_state + college.room_and_board
            if result[y + '.admissions.sat_scores.average.overall'] is not None:
                college.sat_score_average_overall = result[y + '.admissions.sat_scores.average.overall']
            if result[y + '.admissions.act_scores.midpoint.cumulative'] is not None:
                college.act_score_average_overall = result[y + '.admissions.act_scores.midpoint.cumulative']
            if result[y + '.student.share_firstgeneration'] is not None:
                college.first_generation_percentage = round(result[y + '.student.share_firstgeneration']*100,2)
            if result[y + '.student.demographics.race_ethnicity.white'] is not None:
                college.race_white = round(result[y + '.student.demographics.race_ethnicity.white']*100,2)
            if result[y + '.student.demographics.race_ethnicity.black'] is not None:
                college.race_black = round(result[y + '.student.demographics.race_ethnicity.black']*100,2)
            if result[y + '.student.demographics.race_ethnicity.hispanic'] is not None:
                college.race_hispanic = round(result[y + '.student.demographics.race_ethnicity.hispanic']*100,2)
            if result[y + '.student.demographics.race_ethnicity.asian'] is not None:
                college.race_asian= round(result[y + '.student.demographics.race_ethnicity.asian']*100,2)
            if result[y + '.student.demographics.race_ethnicity.aian'] is not None:
                college.race_american_indian = round(result[y + '.student.demographics.race_ethnicity.aian']*100,2)
            if result[y + '.student.demographics.race_ethnicity.nhpi'] is not None:
                college.race_native_hawaiian = round(result[y + '.student.demographics.race_ethnicity.nhpi']*100,2)
            if result[y + '.student.demographics.race_ethnicity.non_resident_alien'] is not None:
                college.race_international = round(result[y + '.student.demographics.race_ethnicity.non_resident_alien']*100,2)


            #will only show in-state net price if instiution is public and in CA
            inst_type_to_get = college.institution_type if college.school_state == 'CA' and result['school.ownership_peps'] == 1\
                else 'private'
            college.net_price_0_30000 = result[y+'.cost.net_price.'+inst_type_to_get+'.by_income_level.0-30000']
            college.net_price_30001_48000 = result[y+'.cost.net_price.'+inst_type_to_get+'.by_income_level.30001-48000']
            college.net_price_48001_75000 = result[y+'.cost.net_price.'+inst_type_to_get+'.by_income_level.48001-75000']
            college.net_price_75001_110000 = result[y+'.cost.net_price.'+inst_type_to_get+'.by_income_level.75001-110000']
            college.net_price_110001_plus = result[y+'.cost.net_price.'+inst_type_to_get+'.by_income_level.110001-plus']

            ivy_leagues = {'Cornell University', 'Dartmouth University', 'Brown University', 'Columbia University',
                'University of Pennsylvania', 'Princeton University', 'Yale University', 'Harvard University'}

            if college.description == '':
                default = (college.institution_type).capitalize() + ' Instiution in ' + college.school_state
                college.description = 'Ivy League Institution' if college.name in ivy_leagues else default   
            
            # get school colors
            school_color_data = College.get_school_color_data()
            school_colors = College.get_school_colors(college.name, school_color_data)
            if school_colors:
                if len(school_colors) > 0:
                    college.school_color1 = school_colors[0]
                if len(school_colors) > 1:
                    college.school_color2 = school_colors[1]
                if len(school_colors) > 2:
                    college.school_color3 = school_colors[2]
                if len(school_colors) > 3:
                    college.school_color4 = school_colors[3]

            return True


    @staticmethod
    def insert_colleges():
        college_names = {
            'University of Pennsylvania', 'Columbia University',
            'Stanford University', 'Princeton University',
            'Harvard University', 'Cornell University', 'Yale University',
            'Brown University', 'Dartmouth College', 'New York University',
            'University of California-Berkeley', 'University of California-Davis',
            'University of California-Los Angeles', 'University of Michigan-Ann Arbor',
            'Carnegie Mellon University', 'John Hopkins University',
            'University of Chicago', 'Amherst College', 'Williams College',
            'Massachusetts Institute of Technology',
            'Georgia Institute of Technology',
            'California Institute of Technology', 'Duke University', 'Pitzer College'
        }
        early_deadlines = [
            datetime(2020, 11, 4),
            datetime(2020, 11, 3),
            datetime(2020, 10, 26),
            datetime(2020, 11, 1),
            datetime(2020, 11, 11),
            datetime(2020, 11, 13),
            datetime(2020, 10, 29)
        ]
        regular_deadlines = [
            datetime(2020, 12, 31),
            datetime(2020, 1, 1),
            datetime(2020, 1, 2),
            datetime(2020, 1, 3),
            datetime(2020, 1, 5),
            datetime(2020, 2, 1),
            datetime(2020, 1, 14)
        ]
        fafsa_deadline = [
            datetime(2020, 12, 31),
            datetime(2020, 1, 1),
            datetime(2020, 1, 2),
            datetime(2020, 1, 3),
            datetime(2020, 1, 5),
            datetime(2020, 2, 1),
            datetime(2020, 1, 14)
        ]
        acceptance_deadline = [
            datetime(2020, 12, 31),
            datetime(2020, 1, 1),
            datetime(2020, 1, 2),
            datetime(2020, 1, 3),
            datetime(2020, 1, 5),
            datetime(2020, 2, 1),
            datetime(2020, 1, 14)
        ]
        scholarship_deadlines = [
            datetime(2020, 12, 31),
            datetime(2020, 1, 1),
            datetime(2020, 1, 2),
            datetime(2020, 1, 3),
            datetime(2020, 1, 5),
            datetime(2020, 2, 1),
            datetime(2020, 1, 14)
        ]

        images = [
            'http://www.collegerank.net/wp-content/uploads/2015/08/morehouse-college-quad.jpg',
            'https://static1.squarespace.com/static/52f11228e4b0a96c7b51a92d/t/55e705bee4b03fc234f02b5e/1441203647587/'
        ]

        for c in college_names:
            college = College.get_college_by_name(c)
            if college is None:
                college = College(
                    name=c,
                    admission_rate = 0,
                    scorecard_id = '',
                    description='',
                    regular_deadline=None,
                    early_deadline=None,
                    fafsa_deadline=None,
                    acceptance_deadline=None,
                    school_url = "",
                    school_size = 0,
                    school_city = "",
                    tuition_in_state = 0,
                    tuition_out_of_state = 0,
                    cost_of_attendance_in_state = 0,
                    cost_of_attendance_out_of_state = 0,
                    room_and_board = 0,
                    sat_score_average_overall = 0,
                    act_score_average_overall = 0,
                    first_generation_percentage = 0,
                    year_data_collected = "",
                    race_white = 0,
                    race_black = 0,
                    race_hispanic = 0,
                    race_asian = 0,
                    race_american_indian = 0,
                    race_native_hawaiian = 0,
                    race_international = 0,
                    scholarship_deadline=None,
                    image=random.choice(images))
                College.retrieve_college_info(college)
            db.session.add(college)
        db.session.commit()

        #@TODOOOOO: DO THE SAME FOR ADD COLLEGE METHOD IN COUNSELOR:VIEWS.PY

    @staticmethod
    def get_school_colors(school_name, school_color_data, _recursed=False):
        '''
        does its best to retrieve the school colors, given the name of a school

        school_name: name of the school as a string
        school_color_data: dictionary of {school names : list of school colors as hex values}
        
        _recursed: do not use, used to determine whether is recursed within function

        returns a list of strings of hex values representing the school colors. 
        '''
        school_name = school_name.replace('university of california', 'uc').\
            replace('university of southern california', 'usc').lower()
        closest_school_name = get_close_matches(school_name, \
                                                [school_color for school_color in school_color_data],n=1)
        if not closest_school_name and not _recursed:
            newer_data = {' '.join(team_name.split()[:-1]) : school_color_data[team_name] \
                        for team_name in school_color_data}
            return College.get_school_colors(school_name.replace('university', '').replace('college', ''), newer_data, \
                                    _recursed=True)
        return school_color_data[closest_school_name[0]] if closest_school_name else None

    @staticmethod
    def get_school_color_data():
        #TODO: import this from pickle file 
        school_color_data = {"abilene christian wildcats": ["4E2683", "FFFFFF", "C5C6C8"], "academy of art urban knights": ["CC0000", "FFFFFF", "000000"], "adams state grizzlies": ["124734", "FFFFFF", "231F20"], "adamson falcons": ["1D3E79", "FFFFFF"], "adelphi panthers": ["4F2C1D", "FFFFFF", "FFB500"], "air force falcons": ["0033A0", "FFFFFF", "8F8F8C"], "akron zips": ["041E42", "FFFFFF", "A89968"], "alabama a&amp;m bulldogs": ["660000", "FFFFFF", "000000"], "alabama crimson tide": ["A60C31", "FFFFFF"], "alabama\u2013huntsville chargers": ["003DA5", "FFFFFF", "29282A"], "alabama state hornets": ["000000", "FFFFFF", "C99700"], "alaska anchorage seawolves": ["00583D", "FFFFFF", "FFC425"], "alaska nanooks": ["236192", "FFFFFF", "FFCD00"], "albany great danes": ["46166B", "FFFFFF", "EEB211"], "albany state golden rams": ["0039A6", "FFFFFF", "EAAB00"], "alberta golden bears": ["284E36", "FFFFFF", "F9B117"], "alcorn state braves": ["46166A", "FFFFFF", "E9A713"], "american eagles": ["005099", "FFFFFF", "C4122E"], "american international yellow jackets": ["000000", "FFFFFF", "FFB60F"], "amherst mammoths": ["332064", "FFFFFF"], "angelo state rams": ["245397", "FFFFFF", "F0C33B"], "appalachian state mountaineers": ["222222", "FFFFFF", "FFCC00"], "arizona state sun devils": ["8C1D40", "FFFFFF", "FFC627"], "arizona wildcats": ["C10230", "FFFFFF", "00205C"], "arkansas\u2013fort smith lions": ["002D56", "FFFFFF", "980038"], "arkansas\u2013monticello boll weevils": ["00965E", "FFFFFF", "000000"], "arkansas-pine bluff golden lions": ["000000", "FFFFFF", "EEB310"], "arkansas razorbacks": ["9D2235", "FFFFFF"], "arkansas state red wolves": ["CC092F", "FFFFFF", "000000"], "arkansas tech wonder boys": ["00533E", "FFFFFF", "FFCE00"], "army black knights": ["2C2A29", "FFFFFF", "D3BC8D", "B1B3B3"], "armstrong state pirates": ["6B212A", "FFFFFF", "FFC400"], "ashland eagles": ["5C068C", "FFFFFF", "FFC72C"], "assumption greyhounds": ["005B99", "FFFFFF", "919693"], "ateneo blue eagles": ["003BAF", "FFFFFF"], "auburn tigers": ["03244D", "FFFFFF", "F26522"], "auburn\u2013montgomery warhawks": ["000000", "FFFFFF", "F04E39"], "augsburg auggies": ["75263B", "FFFFFF", "747678"], "augusta jaguars": ["002F55", "FFFFFF", "A5ACAF"], "augustana university vikings": ["002D62", "FFFFFF", "FFDD00"], "aurora spartans": ["003591", "FFFFFF", "000000"], "austin peay governors": ["BA0C2F", "FFFFFF", "000000"], "avila eagles": ["48176D", "FFFFFF", "8F7E34"], "azusa pacific cougars": ["990000", "FFFFFF", "000000"], "babson beavers": ["006644", "FFFFFF", "000000"], "baker wildcats": ["1E2D50", "FFFFFF", "F4761D"], "ball state cardinals": ["BA0C2F", "FFFFFF", "000000"], "baltimore super bees": ["007DB6", "FFFFFF", "FFB81C"], "barry buccaneers": ["9D1C1F", "FFFFFF", "000000", "D3D4D3"], "barton cougars": ["133C87", "FFFFFF", "B6985A"], "bates bobcats": ["B30838", "FFFFFF", "C4C6C8"], "baylor bears": ["154734", "FFFFFF", "FFB81C"], "belhaven blazers": ["1D3C34", "FFFFFF", "FFD100"], "bellarmine knights": ["660000", "FFFFFF", "CCCCCC"], "belmont bruins": ["00205B", "FFFFFF", "C8102E"], "bemidji state beavers": ["004D44", "FFFFFF", "000000"], "benedict tigers": ["4C145E", "FFFFFF", "F9D616"], "bentley falcons": ["000000", "FFFFFF", "004D99"], "bethany swedes": ["0033A0", "FFFFFF", "FFD100"], "bethel royals": ["002F5F", "FFFFFF", "FDC900"], "bethel threshers": ["9D2235", "FFFFFF", "898D8D"], "bethune\u2013cookman wildcats": ["6F263D", "FFFFFF", "F2A900"], "biola eagles": ["E51636", "FFFFFF", "000000"], "binghamton bearcats": ["005A43", "FFFFFF", "000000"], "birmingham\u2013southern panthers": ["000000", "FFFFFF", "BD8C00"], "black hills state yellow jackets": ["006233", "FFFFFF", "FFC726"], "bloomsburg huskies": ["6E121E", "FFFFFF", "FFDD00"], "boise state broncos": ["0033A0", "FFFFFF", "FA4616"], "boston college eagles": ["8C2232", "FFFFFF", "DBCCA4"], "boston university terriers": ["CC0000", "FFFFFF", "000000"], "bowdoin polar bears": ["000000", "FFFFFF"], "bowling green falcons": ["4F2C1D", "FFFFFF", "FE5000"], "bradley braves": ["A50000", "FFFFFF", "000000"], "brigham young university cougars": ["002E5D", "FFFFFF"], "brown bears": ["4E3629", "FFFFFF", "E03A3E"], "bryant bulldogs": ["231F20", "FFFFFF", "B09863"], "bucknell bison": ["003865", "FFFFFF", "EF5B0C"], "buffalo bulls": ["005BBB", "FFFFFF"], "buffalo state bengals": ["CC6600", "FFFFFF", "000000"], "butler bulldogs": ["13294B", "FFFFFF", "747678"], "byu\u2013hawaii seasiders": ["9E1B34", "FFFFFF", "AA800E"], "calgary dinos": ["E30C00", "FFFFFF", "FFCC00"], "california baptist lancers": ["002554", "FFFFFF", "A37400"], "california golden bears": ["041E42", "FFFFFF", "FFC72C"], "california vulcans": ["DA291C", "FFFFFF", "27251F"], "cal poly mustangs": ["003831", "FFFFFF", "FFE395", "B38F4F"], "cal poly pomona broncos": ["1E4D2B", "FFFFFF", "FFB81C"], "cal state bakersfield roadrunners": ["3154A3", "FFFFFF", "FDB913"], "cal state dominguez hills toros": ["830939", "FFFFFF", "E7B72C"], "cal state east bay pioneers": ["C70C2B", "000000", "FFFFFF"], "cal state fullerton titans": ["00274C", "FFFFFF", "FF7900"], "cal state los angeles golden eagles": ["000000", "FFFFFF", "FFCE00"], "cal state monterey bay otters": ["002A4E", "FFFFFF", "9E8B50"], "cal state northridge matadors": ["CE1126", "FFFFFF", "000000"], "cal state san bernardino coyotes": ["0065BD", "FFFFFF", "000000"], "cal state san marcos cougars": ["007AC3", "FFFFFF", "35B7E9"], "cameron aggies": ["000000", "FFFFFF", "FFC425"], "campbell fighting camels": ["1E252B", "FFFFFF", "EA7125"], "canisius golden griffins": ["0E2756", "FFFFFF", "FFBA00"], "carleton knights": ["0B5091", "FFFFFF", "F3B61D"], "carleton ravens": ["00000D", "FFFFFF", "E31936"], "carlisle indians": ["AE0F0B", "FFFFFF", "CFB53B"], "carnegie tech tartans": ["990000", "FFFFFF", "464646"], "case western reserve spartans": ["0A304E", "FFFFFF", "626262"], "castleton spartans": ["00563B", "FFFFFF", "A4B3BB"], "catawba indians": ["049900", "FFFFFF", "C21630"], "catholic university cardinals": ["990000", "FFFFFF", "000000"], "centenary gentlemen": ["8A2432", "FFFFFF", "000000"], "central arkansas bears": ["4F2D7F", "FFFFFF", "818A8F"], "central connecticut blue devils": ["1A4784", "FFFFFF", "C9CED1"], "central michigan chippewas": ["6A0032", "FFFFFF", "FFC82E"], "central missouri mules": ["CF202E", "FFFFFF", "000000"], "central oklahoma bronchos": ["003366", "FFFFFF", "FFCC00"], "central state marauders": ["71273D", "FFFFFF", "FFCB00"], "central washington wildcats": ["AB0032", "FFFFFF", "2C2A29"], "centre colonels": ["000000", "FFFFFF", "FFCC00"], "chadron state eagles": ["660033", "FFFFFF", "000000"], "chaminade silverswords": ["004990", "FFFFFF", "5E6E66"], "charleston golden eagles": ["992244", "FFFFFF", "FFD200"], "charleston southern buccaneers": ["002855", "FFFFFF", "A89968"], "charlotte 49ers": ["005035", "FFFFFF", "A49665"], "chattanooga mocs": ["00386B", "FFFFFF", "E0AA0F", "ADAFAA"], "cheyney wolves": ["0D3E70", "FFFFFF", "231F20", "2887FF"], "chicago maroons": ["800000", "FFFFFF"], "chicago state cougars": ["006666", "FFFFFF", "000000"], "chico state wildcats": ["952945", "FFFFFF", "AAAAAB"], "christian brothers buccaneers": ["CC092F", "FFFFFF", "A49791"], "christopher newport captains": ["0039A6", "FFFFFF", "84888B"], "cincinnati bearcats": ["E00122", "FFFFFF", "000000"], "citadel bulldogs": ["1F3A60", "FFFFFF", "3975B7"], "city college of new york beavers": ["7D55C7", "000000", "595959"], "claflin panthers": ["000000", "FFFFFF", "CC3727", "570D1A"], "clarion golden eagles": ["003366", "FFFFFF", "97824A"], "clark atlanta panthers": ["CE1126", "FFFFFF", "000000", "444F51"], "clark cougars": ["CC0000", "FFFFFF", "939598"], "clarkson golden knights": ["03522B", "FFFFFF", "FFD204"], "clayton state lakers": ["092C74", "FFFFFF", "FC6719"], "clemson tigers": ["F56600", "FFFFFF", "522D80"], "cleveland state vikings": ["006A4D", "FFFFFF", "000000"], "coastal carolina chanticleers": ["006F71", "FFFFFF", "A27752", "111111"], "colby mules": ["002878", "FFFFFF", "E3D7D1"], "colgate raiders": ["821019", "FFFFFF", "000000"], "colgate red raiders": ["821019", "FFFFFF", "000000"], "columbus state cougars": ["003359", "FFFFFF", "C60C30"], "college of charleston cougars": ["76232F", "FFFFFF", "C5B783"], "colorado a&amp;m aggies": ["006A4D", "FFFFFF", "D9782D"], "colorado buffaloes": ["000000", "FFFFFF", "CFB87C", "A2A4A3"], "colorado christian cougars": ["00416B", "FFFFFF", "FED925"], "colorado college tigers": ["000000", "FFFFFF", "EFAB1E"], "colorado mesa mavericks": ["5D0022", "FFFFFF", "FED103"], "colorado mines orediggers": ["21314D", "FFFFFF", "B2B4B3"], "colorado state rams": ["006A4D", "FFFFFF", "B3A369"], "csu\u2013pueblo thunderwolves": ["00396A", "FFFFFF", "AD123A"], "colorado\u2013colorado springs mountain lions": ["000000", "FFFFFF", "CFB87C"], "columbia lions": ["99CAEA", "000000", "183863", "FFFFFF"], "concordia cavaliers": ["003E7E", "FFFFFF"], "concordia eagles": ["215732", "FFFFFF", "FFCD00"], "concordia golden bears": ["002F65", "FFFFFF", "DEB407"], "connecticut huskies": ["000E2F", "FFFFFF", "E4002B"], "connecticut college camels": ["002F5F", "FFFFFF", "9EC3DE"], "coppin state eagles": ["003056", "FFFFFF", "FFC915"], "cornell big red": ["B31B1B", "FFFFFF", "222222"], "cortland red dragons": ["B91000", "FFFFFF", "000000"], "creighton bluejays": ["00235D", "FFFFFF", "005CA9"], "culinary institute of america steels": ["22693A", "CFAC7F"], "cumberland phoenix": ["98002E", "FFFFFF", "000000"], "daemen wildcats": ["0000FF", "FFFFFF"], "dallas baptist patriots": ["0B1F2C", "FFFFFF", "C41230"], "dartmouth big green": ["00693E", "FFFFFF", "000000"], "davenport panthers": ["D5160C", "FFFFFF", "000000"], "davidson wildcats": ["000000", "FFFFFF", "BF0C26"], "dayton flyers": ["002F87", "FFFFFF", "D70036"], "de la salle green archers": ["00703C", "FFFFFF"], "delaware fightin' blue hens": ["00539F", "FFFFFF", "FFD200"], "delaware state hornets": ["EE3124", "FFFFFF", "0099CC"], "delta state statesmen": ["00753E", "FFFFFF", "000000"], "denver pioneers": ["8B2332", "FFFFFF", "8B6F4B"], "depaul blue demons": ["054696", "FFFFFF", "E4002B"], "depauw tigers": ["111C24", "FFFFFF", "FFCF01"], "detroit mercy titans": ["A6093D", "FFFFFF", "002D72"], "doane tigers": ["FF7900", "FFFFFF", "000000"], "dominican penguins": ["000000", "FFFFFF", "FFB81D"], "dixie state trailblazers": ["BA1C21", "FFFFFF", "002649"], "drake bulldogs": ["003B73", "FFFFFF", "B2B4B3"], "drexel dragons": ["07294D", "FFFFFF", "FFC600"], "drury panthers": ["E31837", "FFFFFF", "6A737B"], "dubuque spartans": ["002D72", "FFFFFF", "999999"], "duke blue devils": ["013088", "FFFFFF"], "duquesne dukes": ["041E42", "FFFFFF", "BA0C2F"], "earlham quakers": ["861F41", "FFFFFF"], "east carolina pirates": ["582C83", "FFFFFF", "FFC72C"], "east central tigers": ["000000", "FFFFFF", "FF5200"], "east stroudsburg warriors": ["DB0436", "FFFFFF", "000000"], "east tennessee state buccaneers": ["041E42", "FFFFFF", "FFC72C"], "eastern arizona gila monsters": ["340265", "FFFFFF"], "eastern illinois panthers": ["003399", "FFFFFF", "B2B2B2"], "eastern kentucky colonels": ["4C151E", "FFFFFF", "B5B5B5"], "eastern michigan eagles": ["046A38", "FFFFFF", "000000"], "eastern new mexico greyhounds": ["006633", "FFFFFF", "A7A9AC"], "eastern washington eagles": ["A10022", "FFFFFF", "000000"], "edinboro fighting scots": ["BB131A", "FFFFFF", "808080"], "elmira soaring eagles": ["3F1E6B", "F1CD44", "86754D"], "elon phoenix": ["73000A", "FFFFFF", "B59A57"], "embry\u2013riddle eagles": ["00549A", "FFFFFF", "FFCD4D"], "emory eagles": ["002878", "FFFFFF", "D28E00"], "emory &amp; henry wasps": ["1B3D75", "FFFFFF", "D5AD28"], "emporia state hornets": ["231F20", "FFFFFF", "BB8D0A"], "endicott gulls": ["00325B", "FFFFFF", "007C5A"], "erskine flying fleet": ["9C1C1F", "FFFFFF", "FFD65D"], "evansville purple aces": ["4C2683", "FFFFFF", "F68B1F"], "fairfield stags": ["E0143E", "FFFFFF", "231F20"], "fairleigh dickinson knights": ["B30838", "FFFFFF", "005596"], "ferris state bulldogs": ["BA0C2F", "FFFFFF", "FFD043"], "feu tamaraws": ["006400", "FFFFFF", "FFD700"], "findlay oilers": ["000000", "FFFFFF", "F47920"], "fitchburg state falcons": ["00563F", "FFFFFF", "E9AF2F"], "flagler saints": ["A52238", "FFFFFF", "F4811F"], "florida a&amp;m rattlers": ["008344", "FFFFFF", "F4811F"], "florida atlantic owls": ["003366", "FFFFFF", "CC0000"], "florida gators": ["003087", "FFFFFF", "FA4616"], "florida gulf coast eagles": ["004785", "FFFFFF", "00794C"], "fiu panthers": ["081E3F", "FFFFFF", "B6862C"], "florida southern moccasins": ["0060A9", "FFFFFF", "E03A3E"], "florida state seminoles": ["782F40", "FFFFFF", "CEB888"], "florida tech panthers": ["770000", "FFFFFF", "9DA0A0"], "fordham rams": ["700429", "FFFFFF", "838070"], "fort hays state tigers": ["000000", "FFFFFF", "FDB913"], "fort lewis skyhawks": ["000066", "FFFFFF", "FFCC33", "0066CC"], "fort valley state wildcats": ["003087", "FFFFFF", "EAAA00"], "fort wayne mastodons": ["003F87", "FFFFFF", "9B9B9C"], "framingham state rams": ["EBAB00", "000000", "FFFFFF"], "francis marion patriots": ["193A80", "FFFFFF", "BB1A1A"], "franklin pierce ravens": ["A91938", "FFFFFF", "6D6E71"], "friends falcons": ["AB0635", "FFFFFF", "444F51"], "fresno pacific sunbirds": ["001F55", "FFFFFF", "FC5D00"], "fresno state bulldogs": ["CC0033", "FFFFFF", "00235D"], "furman paladins": ["582C83", "FFFFFF", "A7A8AA"], "gallaudet bison": ["002A5C", "FFFFFF", "CFAB7A"], "gannon golden knights": ["960A2C", "FFFFFF", "F9A72B"], "gardner\u2013webb runnin' bulldogs": ["A6192E", "FFFFFF", "000000"], "george fox bruins": ["081E3F", "FFFFFF", "BC9C16"], "george mason patriots": ["006633", "FFFFFF", "FFCC33"], "georgetown hoyas": ["041E42", "FFFFFF", "AFA9A0"], "georgetown tigers": ["000000", "FFFFFF", "FF6600"], "george washington colonials": ["00264A", "FFFFFE", "E5D19D"], "georgia bulldogs": ["BA0C2F", "FFFFFF", "000000"], "georgia college bobcats": ["003399", "FFFFFF", "006633"], "georgia southern eagles": ["011E41", "FFFFFF", "87714D"], "georgia southwestern state hurricanes": ["1C3F7B", "FFFFFF", "C69E29"], "georgia state panthers": ["0039A6", "FFFFFF", "CC0000"], "georgia tech yellow jackets": ["B3A369", "000000", "003057", "FFFFFF"], "gonzaga bulldogs": ["041E42", "FFFFFF", "C8102E"], "gordon fighting scots": ["003882", "FFFFFF", "00FFFF"], "graceland yellowjackets": ["00275C", "FFFFFF", "FFCB0B"], "grand canyon antelopes": ["522398", "FFFFFF", "000000"], "grand valley state lakers": ["0033A0", "FFFFFF", "000000"], "grambling state tigers": ["000000", "FFFFFF", "ECAA00"], "grantham talons": ["003366", "D7D7D7"], "green bay phoenix": ["006A4D", "FFFFFF", "183029"], "grinnell pioneers": ["000000", "FFFFFF", "DA291C"], "gustavus adolphus gusties": ["000000", "FFFFFF", "FFCF00"], "hamilton continentals": ["002F86", "FFFFFF", "D6BA8B"], "hamline pipers": ["95021E", "FFFFFF", "BFB9B6"], "hampden\u2013sydney tigers": ["9D183D", "FFFFFF", "B1B7BB"], "hampton pirates": ["265198", "FFFFFF", "A0A0A2"], "hardin\u2013simmons cowboys": ["581483", "FFFFFF", "FFC72C"], "harding bisons": ["000000", "FFFFFF", "CBB778"], "hartford hawks": ["C02427", "FFFFFF", "000000"], "hartwick hawks": ["0033A1", "FFFFFF", "000000"], "harvard crimson": ["A51C30", "FFFFFF", "1E1E1E"], "hawaii\u2013hilo vulcans": ["D81E05", "FFFFFF", "000000"], "hawaii pacific sharks": ["007298", "FFFFFF", "71B1C8"], "hawaii rainbow warriors": ["024731", "FFFFFF", "000000", "B2B2B2"], "henderson state reddies": ["A91D36", "FFFFFF", "000000", "7C7C81"], "high point panthers": ["330072", "FFFFFF", "818183"], "hillsdale chargers": ["004678", "FFFFFF", "ABADBC"], "hobart statesmen": ["472663", "FFFFFF", "FF6418"], "hofstra pride": ["003591", "FFFFFF", "FDC82F"], "holy cross crusaders": ["602D89", "FFFFFF", "AEB2B5"], "holy names hawks": ["C70021", "FFFFFF", "B0B0B0"], "houston baptist huskies": ["00529C", "FFFFFF", "F85512"], "houston cougars": ["C92A39", "FFFFFF", "B8B9B7"], "howard bison": ["003A63", "FFFFFF", "E51937"], "humboldt state lumberjacks": ["046A38", "FFFFFF", "FFC72C"], "hutchinson blue dragons": ["D9293E", "FFFFFF", "004693"], "idaho state bengals": ["F47920", "000000", "000000"], "idaho vandals": ["F1B300", "000000", "808080"], "illinois fighting illini": ["13294B", "FFFFFF", "E84A27"], "illinois college blueboys": ["004A77", "FFFFFF", "828A93"], "illinois state redbirds": ["CE142B", "FFFFFF", "000000"], "incarnate word cardinals": ["CB333B", "FFFFFF", "000000"], "indiana hoosiers": ["990000", "FFFFFF", "EDEBEB"], "indianapolis greyhounds": ["9D2136", "FFFFFF", "C0BFBA"], "indiana state sycamores": ["0C4C91", "FFFFFF", "D0D0CE"], "iona gaels": ["661E2B", "FFFFFF", "EAAF0F"], "iowa hawkeyes": ["000000", "FFFFFF", "FCD116"], "iowa state cyclones": ["822433", "FFFFFF", "FDC82F"], "ithaca bombers": ["003B71", "9C9C9C", "FFBB00"], "iup crimson hawks": ["9E1B32", "FFFFFF", "A2A5A4"], "iupui jaguars": ["990000", "FFFFFF", "F1BE48", "191919"], "ivy league": ["01563F", "FFFFFF"], "jackson state tigers": ["002147", "FFFFFF", "898D8D"], "jacksonville dolphins": ["004E42", "FFFFFF", "C5B783"], "jacksonville state gamecocks": ["CC0000", "FFFFFF", "000000"], "james madison dukes": ["450084", "FFFFFF", "CBB677"], "johns hopkins blue jays": ["68ACE5", "000000", "000000"], "johnson &amp; wales wildcats": ["004680", "FFFFFF", "EAAA00"], "johnson c. smith golden bulls": ["002D56", "FFFFFF", "FFCF01"], "kansas jayhawks": ["0051BA", "FFFFFF", "E8000D"], "kansas state wildcats": ["512888", "FFFFFF", "A7A7A7"], "kansas wesleyan coyotes": ["582C83", "FFFFFF", "FFC72C"], "kean cougars": ["003057", "FFFFFF", "7C878E"], "keene state owls": ["C60C30", "FFFFFF", "000000"], "kennesaw state owls": ["0B1315", "FFFFFF", "FDBB30"], "kent state golden flashes": ["002664", "FFFFFF", "EFAB00"], "kentucky state thorobreds": ["046A38", "FFFFFF", "FFD100"], "kentucky wildcats": ["0033A0", "FFFFFF", "C8C9C7"], "kutztown golden bears": ["782F40", "FFFFFF", "A49473"], "lafayette leopards": ["910029", "FFFFFF", "000000"], "lake erie storm": ["113D2A", "FFFFFF", "000000"], "lake superior state lakers": ["003F87", "FFFFFF", "FFC61E"], "lamar cardinals": ["E31937", "FFFFFF", "000000"], "lander bearcats": ["235782", "FFFFFF", "F8E463"], "lane dragons": ["000080", "FFFFFF", "990000"], "langston lions": ["1B3668", "FFFFFF", "F2682A"], "la salle explorers": ["003057", "FFFFFF", "F1C400"], "lebanon valley flying dutchmen": ["00305C", "FFFFFF", "B2B4B3"], "lee flames": ["0D233F", "FFFFFF", "6F263D"], "lehigh mountain hawks": ["4B2913", "FFFFFF", "C2A875"], "le moyne dolphins": ["00452A", "FFFFFF", "FFF30D"], "lemoyne\u2013owen magicians": ["421383", "FFFFFF", "988344"], "lewis flyers": ["ED174D", "FFFFFF", "000000"], "liberty flames": ["0A254E", "FFFFFF", "990000"], "lincoln blue tigers": ["211C41", "FFFFFF", "929396"], "lincoln memorial railsplitters": ["002461", "FFFFFF", "D1D1CC"], "lindenwood lions": ["000000", "FFFFFF", "DCD087"], "lipscomb bisons": ["331E54", "FFFFFF", "F4AA00"], "little rock trojans": ["6E2639", "FFFFFF", "A7A9AC"], "lock haven bald eagles": ["7A0026", "FFFFFF", "231F20"], "lone star conference": ["002169", "FFFFFF", "E1251B"], "long beach state beach": ["000000", "FFFFFF", "ECAA00"], "liu brooklyn blackbirds": ["231F20", "FFFFFF", "8A8D8F"], "liu post pioneers": ["0E553F", "FFFFFF", "EDAA00"], "liu sharks": ["69B3E7", "000000", "FFC72C"], "longwood lancers": ["041E42", "FFFFFF", "9EA2A2"], "louisiana\u2013lafayette ragin' cajuns": ["CE181E", "FFFFFF", "0A0203"], "louisiana\u2013monroe warhawks": ["840029", "FFFFFF", "FDB913"], "lsu tigers": ["461D7C", "FFFFFF", "FDD023"], "louisiana tech bulldogs": ["003087", "FFFFFF", "CB333B"], "louisiana tech lady techsters": ["69B3E7", "FFFFFF", "CB333B"], "louisville cardinals": ["C9001F", "FFFFFF", "000000"], "lourdes gray wolves": ["B94700", "FFFFFF", "000000"], "loyola greyhounds": ["00694E", "FFFFFF", "CACAC8"], "loyola marymount lions": ["AB0C2F", "FFFFFF", "0076A5"], "loyola ramblers": ["582931", "FFFFFF", "FDB913"], "loyola wolf pack": ["660000", "FFFFFF", "F4AA00"], "lubbock christian chaparrals": ["10147E", "FFFFFF", "F20017"], "macalester scots": ["01426A", "FFFFFF", "D44420"], "maine black bears": ["003263", "FFFFFF", "B0D7FF"], "malone pioneers": ["003E7E", "FFFFFF", "C41230"], "manhattan jaspers": ["00703C", "FFFFFF", "A39161"], "manitoba bisons": ["562E18", "FFFFFF", "B6985E"], "marist red foxes": ["C8102E", "FFFFFF", "231F20"], "mansfield mountaineers": ["D3103E", "FFFFFF", "231F20"], "marquette golden eagles": ["003366", "FFFFFF", "FFCC00"], "marshall thundering herd": ["00B140", "FFFFFF", "231F20"], "martin methodist redhawks": ["A6192E", "FFFFFF", "A28E2A"], "maryland terrapins": ["E21833", "FFFFFF", "FFD200", "000000"], "mary marauders": ["00539B", "FFFFFF", "F58426"], "maryland eastern shore hawks": ["822433", "FFFFFF", "8B8D8E"], "maryville saints": ["C8102E", "FFFFFF", "2C2A29", "FFFFFF"], "massachusetts college of liberal arts trailblazers": ["25408F", "FFFFFF", "A3B86A"], "mcdaniel green terror": ["00674D", "FFFFFF", "F6D016"], "mcgill redmen": ["CD202C", "FFFFFF", "000000"], "mckendree bearcats": ["470A68", "FFFFFF", "B7970C"], "mcneese state cowboys": ["00529B", "FFFFFF", "FFD204"], "mcpherson bulldogs": ["CC0000", "FFFFFF", "000000"], "memphis tigers": ["003087", "FFFFFF", "898D8D"], "mercer bears": ["000000", "FFFFFF", "CB5307"], "mercyhurst lakers": ["006633", "FFFFFF", "003366"], "merrimack warriors": ["003768", "FFFFFF", "F1C400"], "metro state roadrunners": ["00447C", "FFFFFF", "D11242"], "miami hurricanes": ["005030", "FFFFFF", "F05A00"], "miami redhawks": ["B61E2E", "FFFFFF", "000000"], "michigan state spartans": ["18453B", "FFFFFF"], "michigan tech huskies": ["000000", "FFFFFF", "FFCD00"], "michigan wolverines": ["00274C", "FFFFFF", "FFCB05"], "midamerica nazarene pioneers": ["071D49", "FFFFFF", "BF0D3E"], "mid-america intercollegiate athletics association": ["003E7E", "FFFFFF", "D21242"], "middle tennessee state blue raiders": ["0066CC", "FFFFFF", "000000"], "middlebury panthers": ["003882", "FFFFFF"], "midwestern state mustangs": ["862633", "FFFFFF", "EAAA00"], "miles golden bears": ["580D69", "FFFFFF", "E2D000"], "millersville marauders": ["000000", "FFFFFF", "EEB111"], "millsaps majors": ["330066", "FFFFFF", "CCCCCC"], "milwaukee panthers": ["222222", "FFFFFF", "FFB81C"], "minnesota\u2013crookston golden eagles": ["7A0019", "FFFFFF", "FFCC33"], "minnesota\u2013duluth bulldogs": ["7A0019", "FFFFFF", "FFCC33"], "minnesota golden gophers": ["862334", "FFFFFF", "FBB93C"], "minnesota morris cougars": ["8C1919", "FFFFFF", "E19B14"], "minnesota state mavericks": ["480059", "FFFFFF", "F7E400"], "minnesota state\u2013moorhead dragons": ["A6192E", "FFFFFF", "2D2926"], "minot state beavers": ["006341", "FFFFFF", "CC0033"], "occidental tigers": ["000000", "FFFFFF", "FF671F"], "ole miss rebels": ["14213D", "FFFFFF", "CE1126"], "mississippi college choctaws": ["003057", "FFFFFF", "F2A900"], "mississippi state bulldogs": ["5D1725", "FFFFFF"], "mississippi valley state delta devils": ["046A38", "FFFFFF", "C8102E"], "missouri southern lions": ["00693E", "FFFFFF", "F5CF47"], "missouri s&amp;t miners": ["154734", "FFFFFF", "CEB888"], "missouri state bears": ["5E0009", "FFFFFF", "0A141E"], "missouri tigers": ["000000", "FFFFFF", "F1B82D"], "missouri valley conference": ["DF3742", "FFFFFF", "003876"], "missouri western griffons": ["000000", "FFFFFF", "FFC700"], "mit engineers": ["A31F34", "C2C0BF", "8A8B8C"], "monmouth hawks": ["041E42", "FFFFFF", "A5A9AD"], "montana grizzlies": ["660033", "FFFFFF", "999999"], "montana state billings yellowjackets": ["002F5F", "FFFFFF", "F0B310"], "montana state bobcats": ["00205B", "FFFFFF", "BF995B"], "montevallo falcons": ["49176D", "FFFFFF", "FFC423"], "morehead state eagles": ["005EB8", "FFFFFF", "FFCF00"], "morehouse maroon tigers": ["891E31", "FFFFFF", "000000"], "morgan state bears": ["002D74", "FFFFFF", "FF4E00"], "morrisville state mustangs": ["004730", "FFFFFF", "00966C"], "mount mercy mustangs": ["003768", "FFFFFF", "FFDD00"], "mount st. mary's mountaineers": ["002F6C", "FFFFFF", "84754E"], "mount union purple raiders": ["661C78", "FFFFFF", "000000"], "murray state racers": ["002144", "FFFFFF", "ECAC00"], "navy midshipmen": ["000048", "FFFFFF", "B4A87E"], "nebraska cornhuskers": ["E41C38", "FFFFFF", "FDF2D9"], "nebraska\u2013kearney lopers": ["002F6C", "FFFFFF", "CC8A00"], "nevada wolf pack": ["003366", "FFFFFF", "999999"], "newman jets": ["051C48", "FFFFFF", "B32D33"], "new hampshire wildcats": ["041E42", "FFFFFF", "BBBCBC"], "new haven chargers": ["004B8D", "FFFFFF", "FFC425"], "new mexico highlands cowboys": ["502D7F", "FFFFFF", "B2B5B6"], "new mexico lobos": ["BA0C2F", "FFFFFF", "A7A8AA"], "new mexico state aggies": ["891216", "FFFFFF", "CCCCCC"], "new orleans privateers": ["005CA6", "FFFFFF", "A3A9AD", "002F56"], "niagara purple eagles": ["582C83", "FFFFFF", "C7C8CA"], "nicholls state colonels": ["C41230", "FFFFFF", "B2B2B2"], "njit highlanders": ["CC0000", "FFFFFF", "071D49"], "norfolk state spartans": ["007A53", "FFFFFF", "F2A900"], "north alabama lions": ["46166B", "FFFFFF", "B5A268"], "north carolina a&amp;t aggies": ["004684", "FFFFFF", "FDB927"], "north carolina central eagles": ["862633", "FFFFFF", "898D8D"], "nc state wolfpack": ["CC0000", "FFFFFF", "000000"], "north carolina tar heels": ["7BAFD4", "FFFFFF", "13294B"], "north dakota fighting hawks": ["009A44", "FFFFFF", "000000"], "north dakota state bison": ["005643", "FFFFFF", "FFC82E"], "north florida ospreys": ["00246B", "FFFFFF", "D9D9D9"], "north georgia nighthawks": ["002F87", "FFFFFF", "FFC82E"], "north greenville crusaders": ["000000", "FFFFFF", "D60036"], "north texas mean green": ["00853E", "FFFFFF", "231F20"], "northeast conference": ["0D67A4", "FFFFFF", "000000"], "northeastern huskies": ["D41B2C", "FFFFFF", "000000"], "northeastern state riverhawks": ["276444", "FFFFFF", "999999"], "northern arizona lumberjacks": ["003466", "FFFFFF", "FFD200"], "northern colorado bears": ["013C65", "FFFFFF", "F6B000"], "northern illinois huskies": ["BA0C2F", "FFFFFF", "27251F"], "northern iowa panthers": ["4B116F", "FFFFFF", "FFCC00"], "northern kentucky norse": ["000000", "FFFFFF", "FFC82E"], "northern michigan wildcats": ["095339", "FFFFFF", "FFC425"], "northern state wolves": ["990033", "FFFFFF", "FFCC66"], "northwestern oklahoma state rangers": ["000000", "FFFFFF", "CC092F"], "northwestern state demons": ["492F92", "FFFFFF", "F78426"], "northwestern wildcats": ["4E2A84", "FFFFFF", "000000"], "northwest missouri state bearcats": ["006A4E", "FFFFFF", "BABBBC"], "northwest nazarene nighthawks": ["B51946", "FFFFFF", "000000", "4B5457"], "northwood timberwolves": ["093161", "FFFFFF", "0080C3"], "norwich cadets": ["87212E", "907C4B", "000000"], "notre dame de namur argonauts": ["003263", "FFFFFF", "DAC792"], "notre dame fighting irish": ["0C2340", "FFFFFF", "C99700"], "nova southeastern sharks": ["003893", "FFFFFF", "666D70"], "nu bulldogs": ["373C96", "FFFFFF", "D9B638"], "nyit bears": ["242C39", "FFFFFF", "F2AF31"], "nyu violets": ["57068C", "FFFFFF", "000000"], "oakland golden grizzlies": ["000000", "FFFFFF", "B59A57"], "oberlin yeomen": ["CF102D", "FFFFFF", "FFB81D"], "oglethorpe stormy petrels": ["000000", "FFFFFF", "FFDD00"], "ohio bobcats": ["00694E", "FFFFFF"], "ohio dominican panthers": ["000000", "FFFFFF", "FFC72C"], "ohio state buckeyes": ["CE0F3D", "FFFFFF", "B0B7BC"], "oklahoma baptist bison": ["255F2B", "FFFFFF", "FCAF17"], "oklahoma christian eagles": ["660000", "FFFFFF", "CCCCCC"], "oklahoma city stars": ["004B87", "FFFFFF", "000000"], "oklahoma panhandle state aggies": ["001F5B", "FFFFFF", "CF0A2C"], "oklahoma sooners": ["841617", "FFFFFF", "DDCBA4"], "oklahoma state cowboys": ["FE5C00", "FFFFFF", "000000"], "oklahoma wesleyan eagles": ["071D49", "FFFFFF", "9D2235"], "old dominion monarchs": ["00325B", "FFFFFF", "969C9E", "A1D1F1"], "omaha mavericks": ["000000", "FFFFFF", "D71920"], "oral roberts golden eagles": ["002F60", "FFFFFF", "CFB67C"], "oregon ducks": ["036936", "FFFFFF", "FEE11A"], "oregon state beavers": ["D73F09", "FFFFFF", "000000"], "ottawa braves": ["000000", "FFFFFF", "FFBE29"], "ottawa gee-gees": ["651D32", "FFFFFF", "A7A8AA"], "ouachita baptist tigers": ["552988", "FFFFFF", "FFC627"], "pace setters": ["00337F", "FFFFFF", "FFC61E"], "pacific tigers": ["000000", "FFFFFF", "F47920"], "paine lions": ["59178A", "FFFFFF"], "penn quakers": ["011F5B", "FFFFFF", "990000"], "penn state nittany lions": ["001E44", "FFFFFF"], "pepperdine waves": ["00205C", "FFFFFF", "EE7624"], "peru state bobcats": ["0D4D92", "FFFFFF", "D3D3D3"], "pittsburg state gorillas": ["CC0C2F", "FFFFFF", "FCD116"], "pittsburgh panthers": ["003594", "FFFFFF", "FFB81C"], "pittsburgh\u2013johnstown mountain cats": ["1C2957", "FFFFFF", "CDB87D"], "plymouth state panthers": ["135841", "FFFFFF", "000000"], "point loma nazarene sea lions": ["0E553F", "FFFFFF", "FDB827"], "point skyhawks": ["00407A", "FFFFFF", "FCC917"], "portland pilots": ["330072", "FFFFFF"], "portland state vikings": ["154734", "FFFFFF", "A5ACAF"], "prairie view panthers": ["4F2582", "FFFFFF", "FEC325"], "presbyterian blue hose": ["0060A9", "FFFFFF", "9D2235"], "princeton tigers": ["000000", "FFFFFF", "FF6000"], "providence friars": ["000000", "FFFFFF", "8A8D8F"], "purdue boilermakers": ["000000", "FFFFFF", "CFB991"], "purdue fort wayne mastodons": ["000000", "FFFFFF", "C28E0E"], "purdue\u2013northwest pride": ["000000", "FFFFFF", "E6D395"], "quincy hawks": ["581E00", "FFFFFF", "FFD457"], "quinnipiac bobcats": ["0A2240", "FFFFFF", "FFB819"], "radford highlanders": ["C2011B", "FFFFFF", "003C71"], "ramapo roadrunners": ["87212E", "FFFFFF", "000000"], "randolph\u2013macon yellow jackets": ["000000", "FFFFFF", "F9DC30"], "regina rams": ["004F2E", "FFFFFF", "FFC82E"], "regis rangers": ["002B49", "FFFFFF", "F1C400"], "rhode island rams": ["74B4E6", "FFFFFF", "15213B"], "rice owls": ["00205B", "FFFFFF", "C1C6C8"], "richmond spiders": ["002B5E", "FFFFFF", "C32032"], "rider broncs": ["981E32", "FFFFFF", "6C6F70"], "rit tigers": ["F76902", "FFFFFF", "000000"], "robert morris colonials": ["14234B", "FFFFFF", "A6192E"], "rochester yellowjackets": ["003B71", "FFFFFF", "FFD100"], "rockhurst hawks": ["0046AD", "FFFFFF", "000000"], "roger williams hawks": ["003D6E", "E0AD12", "FFFFFF"], "rogers state hillcats": ["002244", "FFFFFF", "B71234"], "rollins tars": ["0071BA", "FFFFFF", "FACF00"], "rowan profs": ["3F1A0A", "FFFFFF", "EDD51C"], "rensselaer polytechnic institute engineers": ["E2231B", "FFFFFF", "222222"], "rutgers university scarlet knights": ["CC0033", "FFFFFF", "000000"], "ryerson rams": ["002D72", "FFFFFF", "D9D9D9"], "sacramento state hornets": ["043927", "FFFFFF", "C4B581"], "sacred heart pioneers": ["CD1041", "FFFFFF", "3C3C3C"], "saginaw valley state cardinals": ["AC162A", "FFFFFF", "003663"], "saint anselm hawks": ["143E5F", "FFFFFF", "CCD6DC"], "saint benedict blazers": ["BE0F34", "FFFFFF", "000000"], "saint francis red flash": ["BD1F25", "FFFFFF", "000000"], "saint john's johnnies": ["BE0F34", "FFFFFF", "5A7E92"], "saint joseph's hawks": ["9E1B32", "FFFFFF", "BCBDC0"], "saint leo lions": ["205C40", "FFFFFF", "F2A900"], "saint louis billikens": ["003DA5", "FFFFFF", "C8C9C7"], "saint martin's saints": ["BF0C26", "FFFFFF", "000000"], "saint mary spires": ["0D223F", "FFFFFF", "FFD101"], "saint mary's cardinals": ["C8102E", "FFFFFF", "002855"], "saint mary's gaels": ["06315B", "FFFFFF", "D80024", "8A8D8F"], "saint michael's purple knights": ["5E2278", "FFFFFF", "DACD96"], "saint peter's peacocks": ["2C2A29", "FFFFFF", "0072CE"], "saint rose golden knights": ["000000", "FFFFFF", "F9B50A"], "salve regina seahawks": ["0069AA", "FFFFFF", "000000"], "samford bulldogs": ["0C2340", "FFFFFF", "BA0C2F"], "sam houston state bearkats": ["FE5000", "FFFFFF"], "san diego state aztecs": ["C41230", "FFFFFF", "000000"], "san diego toreros": ["003B70", "FFFFFF", "75BEE9"], "san francisco dons": ["00543C", "FFFFFF", "FDBB30"], "san francisco state gators": ["52247F", "FFFFFF", "FFCC00"], "san jose state spartans": ["0038A8", "FFFFFF", "FFB81A"], "santa clara broncos": ["862633", "FFFFFF", "000000"], "saskatchewan huskies": ["00693E", "FFFFFF", "000000"], "savannah state tigers": ["002294", "FFFFFF", "F24D17"], "scranton royals": ["4A245E", "FFFFFF", "000000"], "seattle pacific falcons": ["7B1416", "FFFFFF", "000000"], "seattle redhawks": ["AA0000", "FFFFFF", "000000"], "seton hall pirates": ["004488", "FFFFFF", "8A8D8F"], "seton hill griffins": ["BF0033", "FFFFFF", "FCD06B"], "sewanee tigers": ["582C83", "FFFFFF", "CEB888"], "shippensburg red raiders": ["002395", "FFFFFF", "E00034"], "shorter hawks": ["0068B3", "FFFFFF", "231F20"], "siena saints": ["006747", "FFFFFF", "FFC20F"], "simon fraser clan": ["CC0633", "FFFFFF"], "sioux falls cougars": ["492F91", "FFFFFF", "000000"], "skidmore thoroughbreds": ["006A52", "FFFFFF", "FFD100"], "slippery rock the rock": ["006951", "FFFFFF", "000000"], "sonoma state seawolves": ["003366", "FFFFFF", "99BFE6"], "south alabama jaguars": ["00205B", "FFFFFF", "BF0D3E"], "south carolina gamecocks": ["73000A", "FFFFFF", "000000"], "south carolina\u2013beaufort sand sharks": ["061844", "FFFFFF", "E2C081", "8E001C"], "south carolina state bulldogs": ["841A2B", "FFFFFF", "1E4692"], "south dakota coyotes": ["AD0000", "FFFFFF", "000000"], "south dakota mines hardrockers": ["071D49", "FFFFFF", "B3A369"], "south dakota state jackrabbits": ["0032A0", "FFFFFF", "FFD100"], "southeastern fire": ["000000", "FFFFFF", "E31B23"], "southeastern louisiana lions": ["006341", "FFFFFF", "EAAA00"], "southeastern oklahoma state savage storm": ["0033A0", "FFFFFF", "FFDD00"], "southeast missouri state redhawks": ["C8102E", "FFFFFF", "000000"], "southern arkansas muleriders": ["003DA5", "FFFFFF", "FFD100"], "southern connecticut fighting owls": ["001489", "FFFFFF", "97999B"], "southern illinois salukis": ["660000", "FFFFFF", "000000"], "southern maine huskies": ["1E3B78", "FFFFFF", "FFCC00"], "southern new hampshire penmen": ["1A326C", "FFFFFF", "FAB20B"], "southern oregon raiders": ["C8102E", "FFFFFF", "000000"], "siu edwardsville cougars": ["CC0000", "FFFFFF", "000000"], "southern indiana screaming eagles": ["002856", "FFFFFF", "CF102D"], "southern jaguars": ["05356E", "FFFFFF", "FFC72C", "69B3E7"], "smu mustangs": ["CC0035", "FFFFFF", "354CA1"], "southern miss golden eagles": ["000000", "FFFFFF", "FFD046"], "southern nazarene crimson storm": ["891717", "FFFFFF", "000000"], "southern utah thunderbirds": ["C41425", "FFFFFF", "231F20"], "south florida bulls": ["006747", "FFFFFF", "CFC493"], "southwest baptist bearcats": ["4A217E", "FFFFFF", "C2C6C7"], "southwest minnesota state mustangs": ["3A1807", "FFFFFF", "BCAA71"], "southwestern moundbuilders": ["8031A7", "FFFFFF", "000000"], "southwestern pirates": ["000000", "FFFFFF", "FFCC33"], "southwestern oklahoma state bulldogs": ["1B365D", "FFFFFF", "888B8D"], "spring hill badgers": ["49176D", "FFFFFF"], "st. bonaventure bonnies": ["54261A", "FFFFFF", "FDB726"], "st. catherine wildcats": ["491A6A", "FFFFFF", "F7D465"], "st. cloud state huskies": ["A10209", "FFFFFF", "000000"], "st. edward's hilltoppers": ["002566", "FFFFFF", "998F4D"], "st. francis brooklyn terriers": ["0038A8", "FFFFFF", "CE1126"], "st. john's red storm": ["C3002F", "FFFFFF", "011E41"], "saint joseph's pumas": ["41136C", "FFFFFF", "7C1237"], "st. lawrence saints": ["AF1E2D", "FFFFFF", "4B2B23"], "st. mary's rattlers": ["004C97", "FFFFFF", "F2C75C"], "st. olaf oles": ["CC8A00", "000000", "FFFFFF"], "stanford cardinal": ["8C1515", "FFFFFF"], "stanislaus state warriors": ["E31B23", "FFFFFF", "BFB241"], "stephen f. austin lumberjacks": ["3F2A55", "FFFFFF", "B1B3B3"], "sterling warriors": ["9B2743", "FFFFFF", "041E42"], "stetson hatters": ["006747", "FFFFFF", "000000"], "stillman tigers": ["16304B", "FFFFFF", "C5B358"], "stony brook seawolves": ["990000", "FFFFFF", "16243E", "9BA1A6"], "stonehill skyhawks": ["2F2975", "FFFFFF", "17438A", "B9B8B8"], "suffolk rams": ["142F53", "FFFFFF", "C6A141"], "suny brockport golden eagles": ["00533E", "FFFFFF", "FFC726"], "suny canton roos": ["004B8D", "00A160", "CFAB7A"], "suny geneseo knights": ["003896", "FFFFFF", "85888B"], "suny oswego lakers": ["235937", "FFFFFF", "FFCC33"], "suny plattsburgh cardinals": ["C8102E", "FFFFFF", "000000"], "suny potsdam bears": ["8A1538", "FFFFFF", "A2AAAD"], "syracuse orange": ["D44500", "FFFFFF", "0C233F"], "tabor bluejays": ["002D72", "FFFFFF", "FFCD00"], "tampa spartans": ["000000", "FFFFFF", "C8102E", "FFCD00"], "tarleton state texans": ["4F2D7F", "FFFFFF", "000000"], "temple owls": ["990033", "FFFFFF", "222222"], "tennessee volunteers": ["FF8200", "000000", "58595B", "FFFFFF"], "tennessee lady volunteers": ["FF8200", "000000", "006C93", "FFFFFF"], "ut martin skyhawks": ["002649", "FFFFFF", "F77F00"], "tennessee state tigers": ["00539F", "FFFFFF", "D2232A"], "tennessee tech golden eagles": ["4F2984", "FFFFFF", "FFDD00"], "texas a&amp;m aggies": ["500000", "FFFFFF"], "texas a&amp;m\u2013commerce lions": ["0A2846", "FFFFFF", "EDAC09"], "texas a&amp;m international dustdevils": ["61162D", "FFFFFF", "CCCCCC"], "texas a&amp;m\u2013corpus christi islanders": ["0067C5", "FFFFFF", "007F3E"], "texas a&amp;m\u2013kingsville javelinas": ["005DAA", "FFFFFF", "FCC01F"], "texas\u2013arlington mavericks": ["0064B1", "FFFFFF", "F58025"], "texas\u2013permian basin falcons": ["E35205", "FFFFFF", "000000"], "texas\u2013pan american broncs": ["006600", "FFFFFF", "FF6600"], "tcu horned frogs": ["4D1979", "FFFFFF"], "texas longhorns": ["BF5700", "FFFFFF"], "texas southern tigers": ["6F263D", "FFFFFF", "A2AAAD"], "texas state bobcats": ["501214", "FFFFFF", "8D734A"], "texas tech red raiders": ["CC0000", "FFFFFF", "000000"], "texas woman's pioneers": ["850928", "FFFFFF", "000000"], "tiffin dragons": ["00623B", "FFFFFF", "FFF14F"], "toledo rockets": ["003E7E", "FFFFFF", "FFD200"], "towson tigers": ["000000", "FFFFFF", "FFCC00"], "transylvania pioneers": ["B20D35", "FFFFFF", "231F20"], "trinity bantams": ["00305C", "FFFFFF", "F7D117"], "trinity tigers": ["723130", "FFFFFF", "BBBCBC"], "troy trojans": ["6D0017", "FFFFFF", "B2B3B5", "000000"], "truman bulldogs": ["470A68", "FFFFFF", "000000"], "tufts jumbos": ["3E8EDE", "FFFFFF", "512C1D"], "tulane green wave": ["005837", "FFFFFF", "00A4D7"], "tulsa golden hurricane": ["003366", "FFFFFF", "F5002E", "E0CE78"], "tuskegee golden tigers": ["7B0707", "FFFFFF", "F2BD2C"], "uab blazers": ["1E6B52", "FFFFFF", "CFC580"], "ubc thunderbirds": ["002145", "FFFFFF", "F2A900"], "uc davis aggies": ["002855", "FFFFFF", "B3A369"], "ucf knights": ["000000", "FFFFFF", "B7A369"], "uc irvine anteaters": ["0C2340", "FFFFFF", "FFC72C"], "uc los angeles bruins": ["2D68C4", "FFFFFF", "F2A900"], "uc riverside highlanders": ["2D6CC0", "FFFFFF", "F1AB00"], "uc santa barbara gauchos": ["004D9F", "FFFFFF", "FFB814"], "uc santa cruz banana slugs": ["0F1640", "FFFFFF", "E0A600"], "uc san diego tritons": ["182B49", "FFFFFF", "FFCD00"], "ue red warriors": ["ED2939", "FFFFFF"], "uic flames": ["091F40", "FFFFFF", "AC1E2D"], "uhv jaguars": ["E81C18", "FFFFFF", "CCA77C"], "uis prairie stars": ["0C2340", "FFFFFF", "A89968"], "umass boston beacons": ["005A8B", "FFFFFF", "A0CFEB"], "umass dartmouth corsairs": ["003764", "FFFFFF", "FEC24D"], "umass lowell river hawks": ["00549F", "FFFFFF", "CF202F"], "umass minutemen": ["971B2F", "FFFFFF", "272521"], "umbc retrievers": ["000000", "FFFFFF", "FDB515"], "kansas city roos": ["004B87", "FFFFFF", "FFC72C"], "umsl tritons": ["B5121B", "FFFFFF", "EEB211"], "unc asheville bulldogs": ["003DA5", "FFFFFF", "000000"], "unc greensboro spartans": ["0F2044", "FFFFFF", "FFB71B"], "unc pembroke braves": ["000000", "FFFFFF", "A67F31"], "unc wilmington seahawks": ["006666", "FFFFFF", "FFD600", "003366"], "union bulldogs": ["AA0C31", "FFFFFF", "231F20"], "union dutchmen": ["822433", "FFFFFF"], "unlv rebels": ["CF0A2C", "FFFFFF", "CAC8C8"], "up fighting maroons": ["7B1113", "FFFFFF", "014421"], "upper iowa peacocks": ["0D1030", "FFFFFF", "689CD3"], "usc trojans": ["9D2235", "FFFFFF", "FFC72C"], "usc aiken pacers": ["75263B", "FFFFFF", "002E62"], "usc upstate spartans": ["046A38", "FFFFFF", "000000"], "ust growling tigers": ["FCBF15", "000000", "231F20", "FFFFFF"], "utah state aggies": ["00263A", "FFFFFF", "8A8D8F"], "utah utes": ["CC0000", "FFFFFF", "000000"], "utah valley wolverines": ["275D38", "FFFFFF", "000000"], "utep miners": ["041E42", "FFFFFF", "FF8200", "B1B3B3"], "utrgv vaqueros": ["00246B", "FFFFFF", "F05023", "00C21D"], "utsa roadrunners": ["002244", "FFFFFF", "DD4814"], "uw\u2013eau claire blugolds": ["2B3E85", "FFFFFF", "EDAC1A"], "valdosta state blazers": ["CC0000", "FFFFFF", "000000"], "valparaiso crusaders": ["381E0E", "FFFFFF", "FFCC00"], "vanderbilt commodores": ["000000", "FFFFFF", "CEB888"], "vcu rams": ["000000", "FFFFFF", "FFB300"], "vermont catamounts": ["005710", "FFFFFF", "FFC20E"], "villanova wildcats": ["00205B", "FFFFFF", "13B5EA"], "virginia cavaliers": ["232D4B", "FFFFFF", "F84C1E"], "virginia tech hokies": ["861F41", "FFFFFF", "E87722"], "vmi keydets": ["AE122A", "FFFFFF", "FFD619"], "wagner seahawks": ["004331", "FFFFFF", "CCCCCC"], "wake forest demon deacons": ["2C2A29", "FFFFFF", "CEB888"], "walsh cavaliers": ["6D0020", "FFFFFF", "B6985A"], "washburn ichabods": ["003A70", "FFFFFF"], "washington huskies": ["330066", "FFFFFF", "E8D3A2"], "washington &amp; jefferson presidents": ["000000", "FFFFFF", "A4343A"], "washington and lee generals": ["003399", "FFFFFF"], "washington state cougars": ["981E32", "FFFFFF", "53565A"], "washington university bears": ["A51417", "FFFFFF", "007360"], "wayne state warriors": ["115E56", "FFFFFF", "C79316"], "wayne state wildcats": ["000000", "FFFFFF", "FBBF22"], "weber state wildcats": ["4B2682", "FFFFFF", "A1A1A4"], "wentworth institute of technology leopards": ["CF142B", "F7D417", "000000"], "wesleyan cardinals": ["D72121", "101820"], "westminster griffins": ["380E56", "FFFFFF", "BC9B6B"], "west alabama tigers": ["A6192E", "FFFFFF", "000000"], "western carolina catamounts": ["592C88", "FFFFFF", "B9975B"], "western new england golden bears": ["003082", "FFFFFF", "E6B012"], "west chester golden rams": ["540E69", "FFFFFF", "FAAA20"], "west coast conference": ["24CAD2", "000000", "000000"], "western colorado mountaineers": ["A71930", "FFFFFF", "565A5C"], "western illinois leathernecks": ["663399", "FFFFFF", "FFCC00"], "western kentucky hilltoppers": ["B01E24", "FFFFFF", "000000"], "western michigan broncos": ["6C4023", "FFFFFF", "B5A167"], "western new mexico mustangs": ["42196F", "FFFFFF", "FEBE10"], "western mustangs": ["512888", "FFFFFF", "63666A"], "western oregon wolves": ["E31837", "FFFFFF", "231F20", "B2B4B2"], "western washington vikings": ["0E2B58", "FFFFFF", "7898C9", "CAC9C9"], "west florida argonauts": ["0072CE", "FFFFFF", "00AF66"], "west georgia wolves": ["0033A1", "FFFFFF", "DB1A21"], "west liberty hilltoppers": ["000000", "FFFFFF", "FFCD33"], "west texas a&amp;m buffaloes": ["581818", "FFFFFF", "000000"], "west virginia mountaineers": ["002855", "FFFFFF", "EAAA00"], "west virginia state yellow jackets": ["000000", "FFFFFF", "C99700"], "westfield state owls": ["00247D", "FFFFFF", "8E774D"], "wichita state shockers": ["27251F", "FFFFFF", "FFCD00"], "widener pride": ["0057B8", "FFFFFF", "FFC845"], "willamette bearcats": ["98002E", "FFFFFF", "B39D6E"], "william jewell cardinals": ["CC0033", "FFFFFF", "231F20"], "william &amp; mary tribe": ["115740", "FFFFFF", "F0B323", "D0D3D4"], "william carey crusaders": ["D01144FFFFFF000000"], "william smith herons": ["00593D", "FFFFFF"], "wilmington quakers": ["024E43", "FFFFFF", "7AB800"], "williams ephs": ["512698", "FFFFFF", "FFD100"], "windsor lancers": ["005596", "FFFFFF", "FFCE00"], "winona state warriors": ["4B08A1", "FFFFFF", "FFCC33"], "winthrop eagles": ["660000", "FFFFFF", "F0B323"], "winston-salem state rams": ["C8102E", "FFFFFF", "000000"], "wisconsin badgers": ["C4012F", "FFFFFF", "000000"], "wisconsin\u2013parkside rangers": ["004631", "FFFFFF", "213629"], "wisconsin\u2013whitewater warhawks": ["502D7F", "FFFFFF", "BABCBE"], "wofford terriers": ["000000", "FFFFFF", "886E4C"], "worcester state lancers": ["003896", "FFFFFF", "F0E07D"], "wright state raiders": ["026937", "FFFFFF", "CEA052"], "wpi engineers": ["AC2B37", "FFFFFF", "A9B0B7"], "wyoming cowboys": ["492F24", "FFFFFF", "FFC425"], "xavier musketeers": ["0C2340", "FFFFFF", "9EA2A2"], "yale bulldogs": ["00356B", "FFFFFF"], "york panthers": ["005EB8", "FFFFFF", "000000"], "young harris mountain lions": ["260053", "FFFFFF", "C7C6C9"], "youngstown state penguins": ["C8102E", "FFFFFF", "000000"]}
        return school_color_data

    def __repr__(self):
        return '<College: {}>'.format(self.name)

    