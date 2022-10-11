from flask import Blueprint, flash, redirect, render_template, url_for #flash - позволяет передавать сообщения между route-ами, 
    #redirect - делает перенаправление пользователя на другую страницу, 
    #url_for - помогает получить url по имени функции, которая этот url обрабатывает
from flask_login import current_user, login_user, logout_user 
    #LoginManager - главный объект во flask_login, занимается менеджемнетом всего процесса логина

from webapp.user.forms import LoginForm
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
