# encoding: utf-8

from flask import Flask, render_template, request, redirect, url_for, session
import config
from models import User, Question, Answer
from exts import db
from decorators import login_required
import csv
import random

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    with open('static/data/2018-05-01_clean.csv', 'rt') as fin:
        cin = csv.reader(fin)
        data = [row for row in cin]
    explorelist = list()
    length = len(data)
    for row in range(0, 6):
        r = random.randint(1, length - 1)
        explorelist.append(data[r])

    image = ["User_1.jpg", "User_2.jpg", "User_3.jpg", "User_4.jpg", "User_5.jpg"]
    # img = image[random.randint(0, 4)]

    context = {
        'questions': Question.query.order_by('-create_time').all()
    }

    return render_template('index.html', ads=explorelist, img=image, **context)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone, User.password ==
                                 password).first()
        if user:
            session['user_id'] = user.id
            # 如果想在31天内都不需要登录
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return u'Phone Number or Password Wrong, Please Check'


@app.route('/regist/', methods=['GET', 'POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # 手机号码验证，如果被注册了就不能用了
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return u'This number has already been Registered'
        else:
            # password1 要和password2相等才可以
            if password1 != password2:
                return u'Not the Same as First Time'
            else:
                user = User(telephone=telephone, username=username, password=password1)
                db.session.add(user)
                db.session.commit()
                # 如果注册成功，就让页面跳转到登录的页面
                return redirect(url_for('login'))


# 判断用户是否登录，只要我们从session中拿到数据就好了   注销函数
@app.route('/logout/')
def logout():
    # session.pop('user_id')
    # del session('user_id')
    session.clear()
    return redirect(url_for('login'))


@app.route('/question/', methods=['GET', 'POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        contact = request.form.get('contact')
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        zipcode = request.form.get('zipcode')
        price = request.form.get('price')
        bath = request.form.get('bath')
        bed = request.form.get('bed')
        content = request.form.get('content')
        question = Question(contact=contact, address=address, city=city, state=state, zipcode=zipcode, price=price,
                            bath=bath, bed=bed, content=content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        question.author = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/detail/<question_id>/')
def detail(question_id):
    question_model = Question.query.filter(Question.id == question_id).first()
    return render_template('detail.html', question=question_model)


@app.route('/add_answer/', methods=['POST'])
@login_required
def add_answer():
    content = request.form.get('answer_content')
    question_id = request.form.get('question_id')
    answer = Answer(content=content)
    user_id = session['user_id']
    user = User.query.filter(User.id == user_id).first()
    answer.author = user
    question = Question.query.filter(Question.id == question_id).first()
    answer.question = question
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail', question_id=question_id))


@app.route('/search/')
def search():
    q = request.args.get('q')
    # title, content
    # 或 查找方式（通过标题和内容来查找）
    # questions = Question.query.filter(or_(Question.title.contains(q),
    #                                     Question.content.constraints(q))).order_by('-create_time')
    # 与 查找（只能通过标题来查找）
    questions = Question.query.filter(Question.address.contains(q))
    return render_template('index.html', questions=questions)


@app.route('/explore/')
def explore():
    with open('static/data/2018-05-01_clean.csv', 'rt') as fin:
        cin = csv.reader(fin)
        data = [row for row in cin]
    explorelist = list()
    length = len(data)
    for row in range(0, 3):
        r = random.randint(1, length - 1)
        explorelist.append(data[r])
    return render_template('explore.html', explore=explorelist)


# @app.route('/nearbydetails/<full-address>')
# def nearbydetails(full-address):
#
#     return render_template('nearbydetail', )

# 钩子函数(注销)
@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user': user}
    return {}


if __name__ == '__main__':
    app.run(debug=True)
