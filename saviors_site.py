from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from catboost import CatBoost
import pandas as pd

from matrix_generator import prof_predict, get_user_id


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_database.db'
db = SQLAlchemy(app)


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    info = db.Column(db.Text, nullable=True)
    phone_number = db.Column(db.String(30), nullable=True)
    telegram_info = db.Column(db.String(30), nullable=True)
    profession = db.Column(db.String(30), nullable=True)

    def __init__(self,login,password,info,phone_number, telegram_info, profession):
        self.login = login
        self.password = password
        self.info = info
        self.phone_number = phone_number
        self.telegram_info = telegram_info
        self.profession = profession

    def __repr__(self):
        return '<Profile %r>' % self.login


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/registration', methods=['POST','GET'])
def registration():
    if request.method == "POST":
        login = request.form['login']
        password = request.form['password']
        info = request.form['info']
        telegram_info = request.form['telegram_info']
        phone_number = request.form['phone_number']
        user_url = request.form['vk_url']
        vk_id = get_user_id(user_url[15:])
        profession = prof_predict(vk_id)[0][0]
        print(login, profession)
        profile = Profile(login=login,password=password,info=info,telegram_info=telegram_info,phone_number=phone_number, profession=profession)


        db.session.add(profile)
        db.session.commit()

        prof_data = pd.read_excel("education_data.xlsx")
        result_data = prof_data[f'{profession}']
        print(result_data)
        return render_template("conclusion.html",prof_name=result_data[6],curs1=result_data[4],curs2=result_data[5],
                                                photo1=result_data[1],photo2=result_data[3],university=result_data[0],college=result_data[2])

    else:
        return render_template("page1.html")


@app.route('/save_changes')
def save_changes():
    return render_template("page1.html")


if __name__ == "__main__":
    app.run(debug=True)