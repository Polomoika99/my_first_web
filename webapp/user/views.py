from distutils.log import error
from flask import Blueprint, flash, redirect, render_template, url_for #flash - позволяет передавать сообщения между route-ами, 
    #redirect - делает перенаправление пользователя на другую страницу, 
    #url_for - помогает получить url по имени функции, которая этот url обрабатывает
from flask_login import current_user, login_user, logout_user 
    #LoginManager - главный объект во flask_login, занимается менеджемнетом всего процесса логина

from webapp import db
from webapp.user.forms import LoginForm, RegistrationForm
from webapp.user.models import User

blueprint = Blueprint('user', __name__, url_prefix='/users')

@blueprint.route('/login')
def login():
    print(current_user)
    if current_user.is_authenticated: 
        return redirect(url_for('news.index')) # Если пользователь уже авторизован и по какой-то причине зашел на /login - перенаправим его на главную:
    title = "Авторизация"
    login_form = LoginForm() # Создался экземпляр логина
    return render_template('user/login.html', page_title=title, form=login_form)



@blueprint.route('/process-login', methods = ['POST']) #По умолчанию route обрабатывает только метод get. Мы хотим только метод POST
def process_login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data) #Запоминаем пользователя, если успешно вошел на сайт
            flash('Вы успешно вошли на сайт') #Создали сообщение
            return redirect(url_for('news.index')) #Переадресовали на главную страницу

    flash('Неправильные имя или пароль')
    return redirect(url_for('user.login'))


@blueprint.route('/logout')
def logout():
    logout_user()
    flash('Вы успешно разлогинились')
    return redirect(url_for('news.index')) #В оригинале return redirect(url_for('index'))

@blueprint.route('/register')
def register():
    if current_user.is_authenticated: 
        return redirect(url_for('news.index')) # Если пользователь уже авторизован и по какой-то причине зашел на /login - перенаправим его на главную:
    title = "Регистрация"
    form = RegistrationForm() # Создался экземпляр логина
    return render_template('user/registration.html', page_title=title, form=form)


@blueprint.route('/process-reg', methods=['POST']) 
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit(): #Если форма валидна (нет ошибок), создаем нового пользователя
        news_user = User(username=form.username.data, email=form.email.data, role='user')
        news_user.set_password(form.password.data)
        db.session.add(news_user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!')
        return redirect(url_for('user.login'))
    else:
        for field, errors in form.errors.items(): #field - название поля (мейл, никнейм), errors - список строк с текстом типа "Пользователь существует"
            for error in errors:
                flash('Ошибка в поле "{}": {}'.format(
                    getattr(form, field).label.text, #getattr - взять аттрибут
                    error
                ))
        return redirect(url_for('user.register'))
