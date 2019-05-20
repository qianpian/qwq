from flask import Blueprint, render_template
from simpledu.models import Course
from simpledu.forms import LoginForm, RegisterForm
from flask import flash
from flask import redirect, url_for
from flask_login import login_user, logout_user, login_required
from simpledu.models import User
from flask import request, current_app
front = Blueprint('front', __name__)


@front.route('/')
def index():
    # 获取参数中传过来的页数
    page = request.args.get('page', default=1, type=int)
    # 生成分页对象
    pagination = Course.query.paginate(
        #第几页
        page=page,
        #每页显示数目
        per_page=current_app.config['INDEX_PER_PAGE'],
        # True报错引发404 Flase返回第一页的 Pagination 对象
        error_out=False
    )
    return render_template('index.html', pagination=pagination)
@front.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user, form.remember_me.data)
        return redirect(url_for('.index'))
        #front.index简写 同下
    return render_template('login.html', form=form)

@front.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('注册成功,请登录!', 'success')
        return redirect(url_for('.login'))  
        #front.login简写 重定向到当前Blueprint下的某个路由器可以这么简写
    return render_template('register.html', form=form)

@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已退出登录', 'success')
    return redirect(url_for('.index')) 
    #front.index简写
