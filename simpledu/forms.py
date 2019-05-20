from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, Email, EqualTo, DataRequired
from simpledu.models import db, User
from wtforms import ValidationError


from wtforms import TextAreaField, IntegerField
from simpledu.models import Course
from wtforms.validators import URL, NumberRange


from flask_ckeditor import CKEditorField



class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(message='用户名不能为空'), Length(3, 24, message='用户名必须在3－24字符之间')])
    email = StringField('邮箱', validators=[DataRequired(message='邮箱不能为空'), Email(message='email地址不合法')])
    password = PasswordField('密码', validators=[DataRequired(message='密码不能为空'), Length(6, 24, message='密码必须在6-24字符之间')])
    repeat_password = PasswordField('重复密码', validators=[DataRequired(message='重复密码不能为空'), EqualTo('password', message='必须与密码一致')])
    submit = SubmitField('提交')

    def create_user(self):
        user = User()
        user.username = self.username.data
        user.email = self.email.data
        user.password = self.password.data
        db.session.add(user)
        db.session.commit()
        return user
    
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经存在')


class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(message='邮箱不能为空'), Email(message='email地址不合法')])
    password = PasswordField('密码', validators=[DataRequired(message='密码不能为空'), Length(6, 24, message='密码必须在6-24字符之间')])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

    def validate_email(self, field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱未注册')

    def validate_password(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误')


class CourseForm(FlaskForm):
    name = StringField('课程名称', validators=[DataRequired(), Length(5, 32)])
    description = TextAreaField('课程简介', validators=[DataRequired(), Length(20, 256)])
    image_url = StringField('封面图片', validators=[DataRequired(), URL()])
    author_id = IntegerField('作者ID', validators=[DataRequired(), NumberRange(min=1, message='无效的用户ID')])
    submit = SubmitField('提交')

    def validate_author_id(self, field):
        if not User.query.get(field.data):
            raise ValidationError('用户不存在')

    def create_course(self):
        course = Course()
        # 使用课程表单数据填充 course 对象
        self.populate_obj(course)
        db.session.add(course)
        db.session.commit()
        return course

    def update_course(self, course):
        self.populate_obj(course)
        db.session.add(course)
        db.session.commit()
        return course


class ChapterForm(FlaskForm):
    name = StringField('章节名', validators=[DataRequired()])
    now = CKEditorField('章节内容', validators=[DataRequired()])
    video_url = StringField('视频链接', validators=[DataRequired(), URL()])
    submit = SubmitField('提交')
   
    def create_chapter(self, course_id):
        chapter = Chapter()
        # 使用课程表单数据填充 course 对象
        self.populate_obj(chapter)
        chapter.course_id = course_id
        db.session.add(chapter)
        db.session.commit()
        return chapter

    def update_chapter(self, chapter):
        self.populate_obj(chapter)
        db.session.add(chapter)
        db.session.commit()
        return chapter

