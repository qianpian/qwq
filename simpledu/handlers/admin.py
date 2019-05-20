from flask import Blueprint, render_template
from simpledu.decorators import admin_required
from flask import request, current_app
from simpledu.models import Course, Chapter


from flask import redirect, url_for, flash
from simpledu.forms import CourseForm


from simpledu.forms import db

from simpledu.forms import ChapterForm




admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
@admin_required
def index():
    return render_template('admin/index.html')


@admin.route('/courses')
@admin_required
def courses():
    page = request.args.get('page', default=1, type=int)
    pagination = Course.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/courses.html', pagination=pagination)


@admin.route('/courses/create', methods=['GET', 'POST'])
@admin_required
def create_course():
    form = CourseForm()
    if form.validate_on_submit():
        form.create_course()
        flash('课程创建成功', 'success')
        return redirect(url_for('admin.courses'))
    return render_template('admin/create_course.html', form=form)



@admin.route('/courses/<int:course_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)
    form = CourseForm(obj=course)
    if form.validate_on_submit():
        form.update_course(course)
        flash('课程更新成功', 'success')
        return redirect(url_for('admin.courses'))
    return render_template('admin/edit_course.html', form=form, course=course)



@admin.route('/courses/<int:course_id>/delete')
@admin_required
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    flash('课程删除成功', 'success')
    return redirect(url_for('admin.courses'))


@admin.route('courses/<int:course_id>/edit/create', methods=['GET', 'POST'])
@admin_required
def create_chapter(course_id):
    form = ChapterForm()
    if form.validate_on_submit():
        form.create_chapter(course_id)
        flash('章节创建成功', 'success')
        return redirect(url_for('admin.edit_course', course_id=course_id))
    return render_template('admin/create_chapter.html', form=form, 
	course_id=course_id)


@admin.route('/courses/<int:course_id>/edit/<int:chapter_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_chapter(course_id, chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    form = ChapterForm(obj=chapter)
    courses = Course
    if form.validate_on_submit():
        form.update_chapter(chapter)
        flash('章节更新成功', 'success')
        return redirect(url_for('admin.edit_course', course_id=course_id))
    return render_template('admin/edit_chapter.html', 
        form=form, 
        course_id=course_id,
        chapter_id=chapter_id 
        )


@admin.route('/courses/<int:course_id>/edit/<int:chapter_id>/delete')
@admin_required
def delete_chapter(course_id, chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    db.session.delete(chapter)
    db.session.commit()
    flash('章节删除成功', 'success')
    return redirect(url_for('admin.edit_chapter', course_id=course_id, chapter_id=chapter_id))
