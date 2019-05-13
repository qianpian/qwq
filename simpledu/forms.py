from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, Email, EqualTo, DataRequired

class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(message='用户名不能为空'), Length(3, 24, message='用户名必须在3－24字符之间')])
    email = StringField('邮箱', validators=[DataRequired(message='邮箱不能为空'), Email(message='email地址不合法')])
    password = PasswordField('密码', validators=[DataRequired(message='密码不能为空'), Length(6, 24, message='密码必须在6-24字符之间')])
    repeat_password = PasswordField('重复密码', validators=[DataRequired(message='重复密码不能为空'), EqualTo('password', message='必须与密码一致')])
    submit = SubmitField('提交')


class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(message='邮箱不能为空'), Email(message='email地址不合法')])
    password = PasswordField('密码', validators=[DataRequired(message='密码不能为空'), Length(6, 24, message='密码必须在6-24字符之间')])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')
