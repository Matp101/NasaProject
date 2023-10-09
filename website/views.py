'''
views.py
How different pages are viewed by different users
'''
#<!-- <a href="mailto:{{ job.email }}?subject=Job%20Application%20-%20{{ job.emailtitle }}&body=Dear%20Hiring%20Manager,%0D%0A%0D%0AI%20would%20like%20to%20apply%20for%20the%20{{ job.emailtitle }}%20position%20at%20{{ job.emailcompany }}.%20Please%20find%20my%20resume%20attached.%0D%0A%0D%0AThank%20you,%0D%0A{{ current_user.first_name if current_user.first_name else 'Your%20Name' }}" class="btn btn-primary">Apply Now</a> -->
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import *
from .forms import *
from . import db
import json
from sqlalchemy.exc import SQLAlchemyError
from urllib.parse import quote
from .variables import *


views = Blueprint('views', __name__)

PAGE_SIZE = 10


def sort_by(sort):
    if sort == 'newest':
        return Projects.date_posted.desc()
    elif sort == 'oldest':
        return Projects.date_posted.asc()
    else:
        return Projects.date_posted.desc()
    
def get_filters():
    posted_after = request.args.get('posted_after') if request.args.get('posted_after') and request.args.get('posted_after') != 'None' else None
    posted_before = request.args.get('posted_before') if request.args.get('posted_before') and request.args.get('posted_before') != 'None' else None
    experience = request.args.get('experience') if request.args.get('experience') and request.args.get('experience') != 'None' else None
    skill = request.args.get('skill') if request.args.get('skill') and request.args.get('skill') != 'None' else None
    filters = {
        'posted_after': posted_after,
        'posted_before': posted_before,
        'experience': experience,
        'skill': skill
    }
    return filters


def filter_results(query, filters):
    if filters['posted_after']:
        query = query.filter(Projects.date_posted >= filters['posted_after'])
    if filters['posted_before']:
        query = query.filter(Projects.date_posted <= filters['posted_before'])
    if filters['experience']:
        query = query.filter(Projects.experience_level == filters['experience'])
    if filters['skill']:
        for proj in query:
            if filters['skill'] not in proj.skills:
                query = query.filter(Projects.project_id != proj.project_id)
    return query

def fix_layout_home(project, desc=True):
    if project == None:
        return None
    proj = project
    #change the skills
    for idx, skill in enumerate(proj.skills):
        skill_index = int(skill) - 1
        proj.skills[idx] = INTERESTS[skill_index][1]
    proj.skills = ', '.join(proj.skills)
    #change the experience level
    experience_index = int(project.experience_level) - 1
    proj.experience_level = EXPERIENCE[experience_index][1]
    #if project.description is too long, truncate it
    if desc:
        if len(proj.description) > 500:
            proj.description = proj.description[:500] + '...'
    return proj

def fix_layout_account(user):
    if user == None:
        return None
    for idx, interest in enumerate(user.interest):
        interest_index = int(interest) - 1
        user.interest[idx] = INTERESTS[interest_index][1]
    experience_index = int(user.experience) - 1
    user.experience = EXPERIENCE[experience_index][1]
    return user

@views.route('/', methods=['GET', 'POST'])
def home():
    users = User.query.all()
    page = request.args.get('page', 1, type=int)
    projects = Projects.query.all()
    per_page = PAGE_SIZE
    project_list = Projects.query.order_by(Projects.date_posted.desc()).paginate(page=page, per_page=per_page)
    filters = get_filters()
    proj_list = filter_results(project_list, filters)
    
    for project in proj_list.items:
        project = fix_layout_home(project)
    return render_template("home.html", user=current_user, users=users, project_list=proj_list, interests=INTERESTS, filters=filters)

@views.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = PAGE_SIZE
    sort_criteria = request.args.get('sort', 'newest')
    sort = sort_by(sort_criteria)
    filters = get_filters()
    search_results = Projects.query.filter(
        Projects.title.contains(query) | Projects.description.contains(query))
    search_results = filter_results(search_results, filters).order_by(sort).paginate(page=page, per_page=per_page)
    if search_results.total == 0:
        search_results = None
    else:
        for project in search_results.items:
            project = fix_layout_home(project)
    return render_template("search_results.html", query=query, search_results=search_results, user=current_user, sort=sort_criteria, interests=INTERESTS, filters=filters)

@views.route('/createproject', methods=['GET', 'POST'])
@login_required
def createproj():
    form = CreateProjectForm()
    form.skills.choices = INTERESTS
    if form.validate_on_submit():
        title = request.form.get('title')
        description = request.form.get('description')
        experience_level = request.form.get('experience_level')
        skills = request.form.getlist('skills')
        project = Projects(title=title, description=description, experience_level=experience_level, skills=skills, user_id=current_user.id)
        db.session.add(project)
        db.session.commit()

        flash('Job listing created successfully!', 'success')
        return redirect(url_for('views.search'))

    return render_template("createproject.html", user=current_user, form=form)

@views.route('/user_page', methods=['GET'])
def user_page():
    if current_user.is_anonymous:
        return redirect(url_for('auth.login'))
    user=fix_layout_account(current_user)
    user_projects = Projects.query.filter_by(user_id=current_user.id).all()
    new_list = user_projects
    for project in new_list:
        project = fix_layout_home(project)
    return render_template("user_page.html", user=user , user_projects=new_list)

@views.route('/project_page', methods=['GET'])
def project_page():
    id = request.args.get('id')
    project = Projects.query.get(id)
    project = fix_layout_home(project, desc=False)
    return render_template("project_page.html", user=current_user, project=project)

@views.route('/deleteproj', methods=['GET', 'POST'])
def deleteproj():
    if current_user.is_anonymous:
        return redirect(url_for('auth.login'))
    id = request.args.get('id')
    project = Projects.query.get(id)
    if project.user_id != current_user.id:
        return redirect(url_for('views.user_page'))
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('views.user_page'))