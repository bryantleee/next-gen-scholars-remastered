from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required
from . import student

@student.route('/checklist')
@login_required
def checklist():
    """Counselor dashboard page."""
    return render_template('student/checklist.html')