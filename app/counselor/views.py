import datetime
from datetime import date
import pytz
from flask import abort, flash, redirect, render_template, url_for, request, jsonify, Flask
from flask_login import current_user, login_required
from flask_rq import get_queue
from .. import db, csrf
from .forms import (ChangeAccountTypeForm, ChangeUserEmailForm, InviteUserForm,
                    NewUserForm, AddChecklistItemForm, AddTestNameForm,
                    EditTestNameForm, DeleteTestNameForm,
                    AddCollegeProfileForm, EditCollegeProfileStep1Form,
                    EditCollegeProfileStep2Form, DeleteCollegeProfileForm,
                    NewSMSAlertForm, EditSMSAlertForm, ParseAwardLetterForm,
                    AddScholarshipProfileForm, EditScholarshipProfileStep1Form,
                    EditScholarshipProfileStep2Form,EditResourceForm, AddResourceForm,
                    DeleteScholarshipProfileForm)
from . import counselor
from ..decorators import counselor_required
from ..decorators import admin_required
from ..email import send_email
from ..models import (Role, User, College, StudentProfile, EditableHTML,
                      ChecklistItem, TestName, College, Notification, SMSAlert,
                      ScattergramData, Acceptance, Scholarship, fix_url, interpret_scorecard_input, 
                      get_colors, Resource, validate_csvs, extract_url_or_name)

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import requests
import os
import datetime
import csv
import io
import logging
import pandas as pd

# TODO: remove before production?
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
app = Flask(__name__)


@counselor.route('/')
@login_required
@counselor_required
def index():
    """Counselor dashboard page."""
    return render_template('counselor/index.html')


@counselor.route('/scholarships')
@login_required
@counselor_required
def scholarships():
    """View all scholarships"""
    scholarships = Scholarship.query.all()
    category_list = ["African-American","Agriculture","Arts-related","Asian","Asian Pacific American","Community Service",
            "Construction Related Fields","Disabled","Engineering","Environmental Interest","Female","Filipino","First Generation College Student",
            "Queer","General","Latinx","Immigrant/AB540/DACA","Interest in Journalism","Japanese","Jewish","Indigenous","Science/Engineering",
            "Student-Athlete","Teaching","Women in Math/Engineering"]
    return render_template('counselor/scholarships.html', scholarships=scholarships, category_list=category_list)

@csrf.exempt
@counselor.route('/upload_scholarships', methods=['GET', 'POST'])
@login_required
@counselor_required
def upload_scholarship_file():
    if request.method == 'POST':
        f = request.files['file']

        stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.reader(stream)
        header_row = True
        for row in csv_input:
            if header_row:
                header_row = False
                continue
            if len(row) >= 11 and any(row):
                # check that there are at least eleven columns
                # and the row is not completely blank
                scholarship_data = Scholarship(
                    name=row[0],
                    description=row[1],
                    deadline=datetime.datetime.strptime(
                        row[2], "%m/%d/%y") if row[2] else None,
                    award_amount = row[3],
                    category = row[4],
                    merit_based = (row[5] == "Yes"),
                    service_based = (row[6] == "Yes" or row[6] == "yes"),
                    need_based = (row[7] == "Yes" or row[7] == "yes"),
                    minimum_gpa = row[8],
                    interview_required = (row[9] == "Yes" or row[9] == "yes"),
                    link = fix_url(row[10])
                )
                db.session.add(scholarship_data)
        db.session.commit()
        return redirect(url_for('counselor.scholarships'))
    return render_template('counselor/upload_scholarships.html')

@counselor.route('/colleges')
@login_required
@counselor_required
def colleges():
    """View all colleges."""
    colleges = College.query.all()
    has_errors = College.query.filter_by(scorecard_id=None).first() is None
    return render_template('counselor/colleges.html', colleges=colleges, has_errors=has_errors)


@csrf.exempt
@counselor.route('/upload_colleges', methods=['GET', 'POST'])
@login_required
@counselor_required
def upload_college_file():
    if request.method == 'POST':
        #read from file
        f = request.files['file']
        stream = io.StringIO(f.stream.read().decode("utf-8"))
        success, df = validate_csvs.validate_college_csv(stream)
        
        if not success:
            message, message_type = df, 'negative'
        else:
            message, message_type = 'Upload successful!', 'positive'
            for row in df.iterrows():
                college_name = row[1]['College']
                college = College.query.filter_by(name=college_name).first()
                if college is None:
                # College didn't already exist in database, so add it.
                    college = College(
                        name=college_name,
                        scorecard_id = '',
                        description=row[1]['Description'],
                        gpa_unweighted_average_overall=row[1]['Unweighted GPA'],
                        regular_deadline=row[1]['Regular Deadline (RD)'].to_pydatetime() if not pd.isnull(row[1]['Regular Deadline (RD)']) else None,
                        early_deadline=row[1]['Early Deadline (ED)'].to_pydatetime() if not pd.isnull(row[1]['Early Deadline (ED)']) else None,
                        scholarship_deadline=row[1]['Scholarship Deadline'].to_pydatetime() if not pd.isnull(row[1]['Scholarship Deadline']) else None,
                        fafsa_deadline=row[1]['FAFSA Deadline'].to_pydatetime() if not pd.isnull(row[1]['FAFSA Deadline']) else None,
                        acceptance_deadline=row[1]['Acceptance Announcement Date'],
                        school_url = "",
                        school_size = 0,
                        school_city = "",
                        tuition_in_state = 0,
                        tuition_out_of_state = 0,
                        cost_of_attendance_in_state = 0,
                        cost_of_attendance_out_of_state = 0,
                        room_and_board = 0,
                        sat_score_average_overall = 0,
                        act_score_average_overall = 0
                    )
                else:
                    college.description=row[1]['Description']
                    college.gpa_unweighted_average_overall=row[1]['Unweighted GPA']
                    college.regular_deadline=row[1]['Regular Deadline (RD)'].to_pydatetime() if not pd.isnull(row[1]['Regular Deadline (RD)']) else None
                    college.early_deadline=row[1]['Early Deadline (ED)'].to_pydatetime() if not pd.isnull(row[1]['Early Deadline (ED)']) else None
                    college.scholarship_deadline=row[1]['Scholarship Deadline'].to_pydatetime() if not pd.isnull(row[1]['Scholarship Deadline']) else None
                    college.fafsa_deadline=row[1]['FAFSA Deadline'].to_pydatetime() if not pd.isnull(row[1]['FAFSA Deadline']) else None
                    college.acceptance_deadline=row[1]['Acceptance Announcement Date']
                College.retrieve_college_info(college)
                db.session.add(college)
            db.session.commit()
        return redirect(url_for('counselor.colleges'))
    return render_template('counselor/upload_colleges.html')


@counselor.route('/new-user', methods=['GET', 'POST'])
@login_required
@counselor_required
def new_user():
    """Create a new user."""
    form = NewUserForm()
    if form.validate_on_submit():
        user = User(
            role=form.role.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=form.password.data,
            confirmed=True)
        if user.role.id == 1:
            user.student_profile=StudentProfile()
        db.session.add(user)
        db.session.commit()
        flash('User {} successfully created'.format(user.full_name()),
              'form-success')
    return render_template('counselor/new_user.html', form=form)

@counselor.route('/invite-user', methods=['GET', 'POST'])
@login_required
@counselor_required
def invite_user():
    """Invites a new user to create an account and set their own password."""
    form = InviteUserForm()
    if form.validate_on_submit():
        user = User(
            role=form.role.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            confirmed=True)
        if user.role.id == 1:
            user.student_profile=StudentProfile()
        db.session.add(user)
        db.session.commit()
        flash('User {} successfully created'.format(user.full_name()),
              'form-success')
    return render_template('counselor/new_user.html', form=form)



@counselor.route('/user/<int:user_id>')
@counselor.route('/user/<int:user_id>/info')
@login_required
@counselor_required
def user_info(user_id):
    """View a user's profile."""
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
    return render_template('counselor/manage_user.html', user=user)


@counselor.route('/user/<int:user_id>/profile')
@login_required
@counselor_required
def view_user_profile(user_id):
    """ See a student's profile - containing all info from DB """
    student = User.query.filter_by(id=user_id).first()
    if student is None:
        abort(404)
    if student.is_admin():
        abort(404)
    if not student.is_student():
        abort(404)
    sat = 'N/A'
    act = 'N/A'
    student_profile = student.student_profile
    if student_profile is not None:
        test_scores = student_profile.test_scores
        for t in test_scores:
            if t.name == 'SAT':
                sat = max(sat, t.score) if sat != 'N/A' else t.score
            if t.name == 'ACT':
                act = max(act, t.score) if act != 'N/A' else t.score
        return render_template(
            'counselor/student_profile.html', user=student, sat=sat, act=act)
    else:
        abort(404)


@counselor.route('/user/<int:user_id>/change-email', methods=['GET', 'POST'])
@login_required
@counselor_required
def change_user_email(user_id):
    """Change a user's email."""
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
    form = ChangeUserEmailForm()
    if form.validate_on_submit():
        user.email = form.email.data
        db.session.add(user)
        db.session.commit()
        flash('Email for user {} successfully changed to {}.'.format(
            user.full_name(), user.email), 'form-success')
    return render_template('counselor/manage_user.html', user=user, form=form)


@counselor.context_processor
def processor():
    def get_essay_statuses(student_profile):
        return list(set([e.status for e in student_profile.essays]))

    def get_colleges(student_profile):
        return ';'.join([c.name for c in student_profile.colleges])

    return dict(
        get_essay_statuses=get_essay_statuses, get_colleges=get_colleges)


@counselor.route('/student_database', methods=['GET', 'POST'])
@login_required
@counselor_required
def student_database():
    """View student database."""
    checklist_form = AddChecklistItemForm()
    if checklist_form.validate_on_submit():
        for assignee_id in checklist_form.assignee_ids.data.split(','):
            result = add_to_cal(
                student_profile_id=assignee_id,
                text=checklist_form.item_text.data,
                deadline=checklist_form.date.data)
            checklist_item = ChecklistItem(
                text=checklist_form.item_text.data,
                assignee_id=assignee_id,
                is_deletable=False,
                creator_role_id=3,
                deadline=checklist_form.date.data,
                cal_event_id=result['event_id'],
                event_created=result['event_created'])
            db.session.add(checklist_item)
            notif_text = '{} {} added "{}" to your checklist'.format(
                current_user.first_name, current_user.last_name,
                checklist_item.text)
            notification = Notification(
                text=notif_text, student_profile_id=assignee_id)
            db.session.add(notification)
        db.session.commit()

        app.logger.error("first time")

        flash('Checklist item added.', 'form-success')
        return redirect(url_for('counselor.student_database'))

    student_profiles = StudentProfile.query.all()
    colleges = College.query.all()
    essay_statuses = ['Incomplete', 'Waiting', 'Reviewed', 'Edited', 'Done']
    return render_template(
        'counselor/student_database.html',
        student_profiles=student_profiles,
        checklist_form=checklist_form,
        colleges=colleges,
        essay_statuses=essay_statuses)


def add_to_cal(student_profile_id, text, deadline):
    # only add checklist items with a deadline to students calendar
    if deadline is None:
        return {"event_id": "1", "event_created": False}
    y = deadline.year
    m = deadline.month
    d = deadline.day
    student_profile = StudentProfile.query.filter_by(
        id=student_profile_id).first()
    if student_profile is None:
        return {"event_id": "1", "event_created": False}
    # if a student has not authorized google calendar yet
    if student_profile.cal_token is None:
        return {"event_id": "1", "event_created": False}
    credentials_json = {
        'token': student_profile.cal_token,
        'refresh_token': student_profile.cal_refresh_token,
        'token_uri': student_profile.cal_token_uri,
        'client_id': student_profile.cal_client_id,
        'client_secret': student_profile.cal_client_secret,
        'scopes': student_profile.cal_scopes
    }

    credentials = google.oauth2.credentials.Credentials(**credentials_json)
    service = googleapiclient.discovery.build(
        'calendar', 'v3', credentials=credentials)
    event = {
        'summary': text,
        'start': {
            'dateTime': datetime.datetime(y, m, d).isoformat('T'),
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': datetime.datetime(y, m, d).isoformat('T'),
            'timeZone': 'America/Los_Angeles',
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    # save the authentication values in case they have been refreshed
    student_profile.cal_token = credentials.token
    student_profile.cal_refresh_token = credentials.refresh_token
    student_profile.cal_token_uri = credentials.token_uri
    student_profile.cal_client_id = credentials.client_id
    student_profile.cal_client_secret = credentials.client_secret
    student_profile.cal_scopes = credentials.scopes
    db.session.add(student_profile)
    db.session.commit()
    return {"event_id": event.get('id'), "event_created": True}


@counselor.route('/_update_editor_contents', methods=['POST'])
@login_required
@counselor_required
def update_editor_contents():
    """Update the contents of an editor."""

    edit_data = request.form.get('edit_data')
    editor_name = request.form.get('editor_name')

    editor_contents = EditableHTML.query.filter_by(
        editor_name=editor_name).first()
    if editor_contents is None:
        editor_contents = EditableHTML(editor_name=editor_name)
    editor_contents.value = edit_data

    db.session.add(editor_contents)
    db.session.commit()

    return 'OK', 200


# order checklist items, soonest deadline is first
# checklists with no deadline appear at the end
def compare_checklist_items(item):
    if item.deadline:
        return item.deadline
    else:
        return date.max


@counselor.route('/default_checklist', methods=['GET', 'POST'])
@login_required
@counselor_required
def default_checklist():
    # display list of default checklist items and option to add a new one
    default_items = ChecklistItem.query.filter_by(is_default_item=True)
    default_items = [item for item in default_items]
    default_items.sort(key=compare_checklist_items)
    form = AddChecklistItemForm()
    if form.validate_on_submit():
        # create new checklist item from form data
        exists = ChecklistItem.query.filter_by(text=form.item_text.data).filter_by(deadline=form.date.data).first()

        if not exists:
            new_item = ChecklistItem(
                text=form.item_text.data,
                assignee_id=current_user.id,
                creator_role_id=3,
                is_default_item=True,
                deadline=form.date.data)
            db.session.add(new_item)

            users = User.query.filter_by(role_id=1)
            for user in users:
                # add new checklist to each user's account
                if (user == users.first()):
                    ite = ChecklistItem.query.filter_by(assignee_id=user.student_profile.id).filter_by(text=form.item_text.data).filter_by(deadline=form.date.data).first()
                    if not ite:
                        checklist_item = ChecklistItem(
                            assignee_id=user.student_profile_id,
                            text=form.item_text.data,
                            is_deletable=False,
                            deadline=form.date.data)
                        db.session.add(checklist_item)
                else:
                    checklist_item = ChecklistItem(
                        assignee_id=user.student_profile_id,
                        text=form.item_text.data,
                        is_deletable=False,
                        deadline=form.date.data)
                    db.session.add(checklist_item)

        db.session.commit()

        users = User.query.filter_by(role_id=1)
        for user in users:
            # add new checklist to each user's account
            checklist_items = ChecklistItem.query.filter_by(assignee_id=user.student_profile_id)
            checklist_items = [item for item in checklist_items if not item.is_checked]
            app.logger.error('adding student stuff')
            app.logger.error(checklist_items)

        return redirect(url_for('counselor.default_checklist'))
    return render_template(
        'counselor/default_checklist.html', form=form, checklist=default_items)


@counselor.route('/add_test', methods=['GET', 'POST'])
@login_required
@counselor_required
def add_test_name():
    # Allows a counselor to add a test name to the database.
    form = AddTestNameForm()
    if form.validate_on_submit():
        test_name = TestName.query.filter_by(name=form.name.data).first()
        if test_name is None:
            # Test didn't already exist in database, so add it.
            test = TestName(name=form.name.data)
            db.session.add(test)
            db.session.commit()
        else:
            flash('Test could not be added - test already exists in the database.',
                  'error')
        return redirect(url_for('counselor.index'))
    return render_template('counselor/add_test_name.html', form=form)


@login_required
@counselor.route(
    '/resources/delete/<int:item_id>', methods=['GET', 'POST'])
@csrf.exempt
def delete_resource(item_id):
    resource = Resource.query.filter_by(id=item_id).first()
    if resource:
        # only allows the counselors/admins to perform action
        if current_user.role_id >= 2:
            db.session.delete(resource)
            db.session.commit()
            return jsonify({"success": "True"})
    return jsonify({"success": "False"})


@counselor.route('/edit_test', methods=['GET', 'POST'])
@login_required
@counselor_required
def edit_test_name():
    # Allows a counselor to edit a test name in the database.
    form = EditTestNameForm()
    if form.validate_on_submit():
        test_name = form.old_test.data
        test_name.name = form.new_name.data
        db.session.add(test_name)
        db.session.commit()
        flash('Test name successfully edited.', 'form-success')
        return redirect(url_for('counselor.index'))
    return render_template(
        'counselor/edit_test_name.html', form=form, header='Edit Test Name')


@counselor.route('/delete_test', methods=['GET', 'POST'])
@login_required
@counselor_required
def delete_test_name():
    # Allows a counselor to delete a test name in the database.
    form = DeleteTestNameForm()
    if form.validate_on_submit():
        test_name = form.old_test.data
        db.session.delete(test_name)
        db.session.commit()
        flash('Test name successfully deleted.', 'form-success')
        return redirect(url_for('counselor.index'))
    return render_template(
        'counselor/delete_test_name.html',
        form=form,
        header='Delete Test Name')

@counselor.route('/add_college', methods=['GET', 'POST'])
@login_required
@counselor_required
def add_college():
    # Allows a counselor to add a college profile.
    form = AddCollegeProfileForm()
    if form.validate_on_submit():
        extracted_value, val_type = extract_url_or_name(form.name.data)
        if val_type == 'scorecard_id':
            college = College.query.filter_by(scorecard_id=extracted_value).first()
        else:
            college = College.query.filter_by(name=extracted_value).first()

        if college is None:
            # College didn't already exist in database, so add it.
            college = College(
                name=extracted_value if val_type == 'name' else '',
                scorecard_id=extracted_value if val_type == 'scorecard_id' else None,
                description=form.description.data,
                gpa_unweighted_average_overall=form.gpa_unweighted_average_overall.data,
                early_deadline=form.early_deadline.data,
                regular_deadline=form.regular_deadline.data,
                scholarship_deadline=form.scholarship_deadline.data,
                fafsa_deadline=form.fafsa_deadline.data,
                acceptance_deadline=form.acceptance_deadline.data,
                school_url = "",
                school_size = 0,
                school_city = "",
                tuition_in_state = 0,
                tuition_out_of_state = 0,
                cost_of_attendance_in_state = 0,
                cost_of_attendance_out_of_state = 0,
                room_and_board = 0,
                sat_score_average_overall = 0,
                act_score_average_overall = 0)
            College.retrieve_college_info(college, change_name=val_type=='scorecard_id')
            db.session.add(college)
        else:
            flash('College could not be added - already exists in database.',
                  'error')
        return redirect(url_for('counselor.colleges'))
    db.session.commit()
    return render_template(
        'counselor/add_college.html', form=form, header='Add College Profile')


@counselor.route('/edit_college', methods=['GET', 'POST'])
@login_required
@counselor_required
def edit_college_step1():
    return redirect(
            url_for('counselor.colleges'))
#     # Allows a counselor to choose which college they want to edit.
#     form = EditCollegeProfileStep1Form()
#     if form.validate_on_submit():
#         college = College.query.filter_by(name=form.name.data.name).first()
#         return redirect(
#             url_for('counselor.edit_college_step2', college_id=college.id))
#     return render_template(
#         'counselor/edit_college.html',
#         form=form,
#         header='Edit College Profile')


@counselor.route('/edit_college/<int:college_id>', methods=['GET', 'POST'])
@login_required
@counselor_required
def edit_college_step2(college_id):
    # Allows a counselor to edit the previously chosen college.
    # This page is one you get re-routed to, not one that's findable.
    old_college = College.query.filter_by(id=college_id).first()
    form = EditCollegeProfileStep2Form(
        name=old_college.name,
        description=old_college.description,
        gpa_unweighted_average_overall=old_college.gpa_unweighted_average_overall,
        regular_deadline=old_college.regular_deadline,
        early_deadline=old_college.early_deadline,
        scholarship_deadline=old_college.scholarship_deadline,
        fafsa_deadline=old_college.fafsa_deadline,
        acceptance_deadline=old_college.acceptance_deadline)
    if form.validate_on_submit():
        college = old_college
        extracted_value, val_type = extract_url_or_name(form.name.data)
        if val_type == 'scorecard_id':
            college.scorecard_id=extracted_value
        else:
            college.name = extracted_value
        college.description = form.description.data
        college.gpa_unweighted_average_overall = form.gpa_unweighted_average_overall.data
        college.early_deadline = form.early_deadline.data
        college.regular_deadline = form.regular_deadline.data
        college.scholarship_deadline = form.scholarship_deadline.data
        college.fafsa_deadline = form.fafsa_deadline.data
        college.acceptance_deadline = form.acceptance_deadline.data
        College.retrieve_college_info(college, change_name=val_type=='scorecard_id')
        db.session.add(college)
        db.session.commit()
        flash('College profile successfully edited.', 'form-success')
        return redirect(url_for('counselor.colleges'))
    return render_template(
        'counselor/edit_college.html',
        college_id=college_id,
        form=form,
        header='Edit College Profile')


@counselor.route('/delete_college', methods=['GET', 'POST'])
@login_required
@counselor_required
def delete_college():
    """Allows a counselor to delete a college profile."""
    form = DeleteCollegeProfileForm()
    if form.validate_on_submit():
        college = form.name.data
        db.session.delete(college)
        db.session.commit()
        flash('College profile successfully deleted.', 'form-success')
        return redirect(url_for('counselor.index'))
    return render_template(
        'counselor/delete_college.html',
        form=form,
        header='Delete College Profile')

@counselor.route('/delete_college/<int:college_id>', methods=['GET', 'POST'])
@login_required
@counselor_required
def delete_specific_college(college_id):
    # Allows a counselor to delete a specific college profile.
    college = College.query.filter_by(id=college_id).first()
    db.session.delete(college)
    db.session.commit()
    return redirect(url_for('counselor.colleges'))


@counselor.route('/alerts', methods=['GET', 'POST'])
@login_required
@counselor_required
def alerts_dashboard():
    """Dashboard to view and add SMS alerts."""
    return render_template('counselor/alerts/alerts_dashboard.html')


@counselor.route('/alerts/manage', methods=['GET', 'POST'])
@login_required
@counselor_required
def manage_alerts():
    """Database of text notifications to send."""
    alerts = SMSAlert.query.order_by(SMSAlert.date).all()
    return render_template(
        'counselor/alerts/manage_alerts.html', alerts=alerts)


@counselor.route('/alerts/add', methods=['GET', 'POST'])
@login_required
@counselor_required
def add_alert():
    """View add alert form."""
    form = NewSMSAlertForm()
    if form.validate_on_submit():
        hour, minute = form.time.data.split(':')
        am_pm = form.am_pm.data
        hour = (int(hour) % 12) + (12 if am_pm == 'PM' else 0)
        alert = SMSAlert(
            title=form.title.data,
            content=form.content.data,
            date=form.date.data,
            time=datetime.time(hour, int(minute)))
        db.session.add(alert)
        db.session.commit()
        flash('Successfully created alert "{}"!'.format(alert.title),
              'form-success')
        return redirect(url_for('counselor.add_alert'))
    return render_template('counselor/alerts/add_alert.html', form=form)


@counselor.route('/alerts/edit/<int:alert_id>', methods=['GET', 'POST'])
@login_required
@counselor_required
def edit_alert(alert_id):
    """Edit alert."""
    alert = SMSAlert.query.filter_by(id=alert_id).first()
    if alert is None:
        abort(404)
    form = EditSMSAlertForm(
        title=alert.title,
        content=alert.content,
        date=alert.date,
        time=alert.time.strftime("%-I:%M"),
        am_pm=alert.time.strftime("%p"))
    if form.validate_on_submit():
        hour, minute = form.time.data.split(':')
        am_pm = form.am_pm.data
        hour = (int(hour) % 12) + (12 if am_pm == 'PM' else 0)
        alert.title = form.title.data
        alert.content = form.content.data
        alert.date = form.date.data
        alert.time = datetime.time(hour, int(minute))
        db.session.add(alert)
        db.session.commit()
        flash('Successfully edit alert "{}"!'.format(alert.title),
              'form-success')
        return redirect(url_for('counselor.edit_alert', alert_id=alert.id))
    return render_template('counselor/alerts/edit_alert.html', form=form)

## HEREEEEE
@csrf.exempt
@counselor.route('/upload_scattergram', methods=['GET', 'POST'])
@login_required
@counselor_required
def upload_scattergram():
    if request.method == 'POST':
        valid_colleges = [college.name for college in College.query.all()]
        valid_students = ['{} {}'.format(user.first_name, user.last_name) for user in User.query.all()]
        
        #read from file
        f = request.files['file']
        stream = io.StringIO(f.stream.read().decode("utf-8"))
        success, df = validate_csvs.validate_scattergram_csv(stream, valid_students, valid_colleges)

        if not success:
            message, message_type = df, 'negative'
        else:
            message, message_type = 'Upload successful!', 'positive'
            for row in df.iterrows():
                point = ScattergramData(
                    name=row[1]['student name'],
                    college=row[1]['college'],
                    status=row[1]['application status'],
                    GPA=row[1]['gpa'],
                    SAT2400=row[1]['sat2400'],
                    SAT1600=row[1]['sat1600'],
                    ACT=row[1]['act']
                )
                db.session.add(point)
            db.session.commit()
        # for name in list(college_names):
        #     college = College.query.filter_by(name=name).first()
        #     if college:
        #         college.update_plots()
       
        return render_template('counselor/upload_scattergram.html', message=message, message_type=message_type)
    return render_template('counselor/upload_scattergram.html', message=None, message_type=None)

@counselor.route('/')
@login_required
@counselor_required
def view_checklist():
    return render_template('account/checklist.html')

# adds parsed award letter information to an acceptance
@csrf.exempt
@counselor.route('/parse_award_letter/<int:item_id>', methods=['GET', 'POST'])
@login_required
@counselor_required
def parse_award_letter(item_id):
    acceptance = Acceptance.query.filter_by(id=item_id).first()
    if acceptance:
        form = ParseAwardLetterForm()
        if form.validate_on_submit():
            acceptance.cost = form.cost.data
            acceptance.loans = form.loans.data
            acceptance.work_study = form.work_study.data
            acceptance.financial_aid = form.financial_aid.data
            acceptance.institutional_scholarships = form.institutional_scholarships.data
            acceptance.net_cost = form.net_cost.data
            db.session.add(acceptance)
            db.session.commit()
            url = url_for('counselor.student_database')
            return redirect(url)
        return render_template(
            'student/edit_academic_info.html',
            form=form,
            header="Parse Award Letter",
            student_profile_id=acceptance.student_profile_id)
    abort(404)


@csrf.exempt
@counselor.route('/acceptance/<int:item_id>', methods=['GET', 'POST'])
@login_required
def view_acceptance_profile(item_id):
    acceptance = Acceptance.query.filter_by(it=item_id).first()
    if acceptance:
        college = College.query.filter_by(name=acceptance.college).first()
        return render_template(
            'student/acceptance_profile.html',
            acceptance=acceptance,
            college=college)
    abort(404)


@csrf.exempt
@counselor.route(
    '/add_scholarship',
    methods=['GET','POST'])
@counselor_required
def add_scholarship():
    form = AddScholarshipProfileForm()
    if form.validate_on_submit():
        name = Scholarship.query.filter_by(name=form.name.data).first()
        if name is None:
            schol = Scholarship(
                name=form.name.data,
                deadline=form.deadline.data,
                award_amount=form.award_amount.data,
                category=form.category.data,
                description=form.description.data,
                merit_based=form.merit_based.data,
                service_based=form.service_based.data,
                need_based=form.need_based.data,
                minimum_gpa=form.minimum_gpa.data,
                interview_required=form.interview_required.data,
                link=fix_url(form.link.data))
            db.session.add(schol)
        else:
            flash('Scholarship could not be added - already exists in database.', 'error')
        return redirect(url_for('counselor.index'))
    db.session.commit()
    return render_template(
        'counselor/add_college.html', form=form, header="Add Scholarship Profile")


@counselor.route('/edit_scholarship', methods=['GET', 'POST'])
@login_required
@counselor_required
def edit_scholarship_step1():
    # Allows a counselor to choose which college they want to edit.
    form = EditScholarshipProfileStep1Form()
    if form.validate_on_submit():
        schol = Scholarship.query.filter_by(name=form.name.data.name).first()
        return redirect(
            url_for('counselor.edit_scholarship_step2', scholarship_id=schol.id))
    return render_template(
        'counselor/edit_scholarship.html',
        form=form,
        header='Edit Scholarship Profile')

@counselor.route('/edit_scholarship/<int:scholarship_id>', methods=['GET', 'POST'])
@login_required
@counselor_required
def edit_scholarship_step2(scholarship_id):
    # Allows a counselor to edit the previously chosen college.
    # This page is one you get re-routed to, not one that's findable.
    old_schol = Scholarship.query.filter_by(id=scholarship_id).first()
    form = EditScholarshipProfileStep2Form(
        name=old_schol.name,
        deadline=old_schol.deadline,
        award_amount=old_schol.award_amount,
        category=old_schol.category,
        description=old_schol.description,
        merit_based=old_schol.merit_based,
        service_based=old_schol.service_based,
        need_based=old_schol.need_based,
        minimum_gpa=old_schol.minimum_gpa,
        interview_required=old_schol.interview_required,
        link=fix_url(old_schol.link))
    if form.validate_on_submit():
        schol = old_schol
        schol.name = form.name.data
        schol.deadline=form.deadline.data
        schol.award_amount=form.award_amount.data
        schol.category=form.category.data
        schol.description=form.description.data
        schol.merit_based=form.merit_based.data
        schol.service_based=form.service_based.data
        schol.need_based=form.need_based.data
        schol.minimum_gpa=form.minimum_gpa.data
        schol.interview_required=form.interview_required.data
        schol.link=fix_url(form.link.data)
        db.session.add(schol)
        db.session.commit()
        flash('Scholarship profile successfully edited.', 'form-success')
        return redirect(url_for('counselor.scholarships'))
    return render_template(
        'counselor/edit_scholarship.html',
        form=form,
        header='Edit Scholarship Profile')

@counselor.route('/delete_scholarship', methods=['GET', 'POST'])
@login_required
@counselor_required
def delete_scholarship():
    """Allows a counselor to delete a scholarship profile."""
    form = DeleteScholarshipProfileForm()
    if form.validate_on_submit():
        scholarship = form.name.data
        db.session.delete(scholarship)
        db.session.commit()
        flash('Scholarship profile successfully deleted.', 'form-success')
        return redirect(url_for('counselor.index'))
    return render_template(
        'counselor/delete_scholarship.html',
        form=form,
        header='Delete Scholarship Profile')


#resources methods

@counselor.route('/resources')
@login_required
def resources():
    """View all Resources."""
    resources = Resource.query.all()
    editable_html_obj = EditableHTML.get_editable_html('resources')
    return render_template('counselor/resources.html', resources=resources, editable_html_obj=editable_html_obj, colors=get_colors())

@login_required
@counselor.route(
    '/resources/edit/<int:item_id>', methods=['GET', 'POST'])
@csrf.exempt
def edit_resource(item_id):
    resource = Resource.query.filter_by(id=item_id).first()
    form = EditResourceForm(
        resource_url=resource.resource_url,
        title=resource.title,
        description=resource.description,
        image_url=resource.image_url
    )
    if not resource:
        abort(404)
    if form.validate_on_submit():
        resource_new = resource
        resource_new.resource_url = form.resource_url.data
        resource_new.title = form.title.data
        resource_new.description = form.description.data
        resource_new.image_url = form.image_url.data
        db.session.add(resource_new)
        db.session.commit()
        flash('Resource successfully edited.', 'form-success')
        return redirect(url_for('counselor.resources'))
    return render_template('counselor/edit_resource.html', form=form,
        resource=resource, header='Edit Resource')

@counselor.route('/add_resource', methods=['GET', 'POST'])
@login_required
@counselor_required
def add_resource():
    # Allows a counselor to add a college profile.
    form = AddResourceForm()
    if form.validate_on_submit():
        resource_url = Resource.query.filter_by(resource_url=form.resource_url.data).first()
        if resource_url is None:
            # College didn't already exist in database, so add it.
            resource = Resource(
                resource_url=form.resource_url.data,
                title=form.title.data,
                description=form.description.data,
                image_url=form.image_url.data
            )
            db.session.add(resource)
        else:
            flash('Resource could not be added - already exists in database.',
                  'error')
        return redirect(url_for('counselor.resources'))
    db.session.commit()
    return render_template(
        'counselor/add_resource.html', form=form, header='Add Resource')
