'''''''''''''''''''''''''''''''''''''''''''''''''''
  > System:		Archlinux
  > Author:		ty-l6
  > Mail:		liuty196888@gmail.com
  > File Name:		first.py
  > Created Time:	2016-12-09 Fri 10:01
'''''''''''''''''''''''''''''''''''''''''''''''''''

import flask
import flask_script
import flask_bootstrap
import flask_moment
import datetime
import flask_wtf
import wtforms
from wtforms import validators
import flask_sqlalchemy
import flask_migrate
import os
import flask_mail
import threading

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'you can never belive it'
bootstrap = flask_bootstrap.Bootstrap(app)

m = flask_moment.Moment(app)
# then the template can use moment, this is a type 
# which exactly is flask_moment._moment

manager = flask_script.Manager(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']= \
        'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = flask_sqlalchemy.SQLAlchemy(app)
migrate = flask_migrate.Migrate(app, db)
manager.add_command('db', flask_migrate.MigrateCommand)

# email
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[lty Flasky]'
app.config['FLASKY_MAIL_SENDER'] = '996651583@qq.com'
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')
mail = flask_mail.Mail(app)

def async_send(message):
    with app.app_context():
        mail.send(msg)
def send_email(to, subject, template_file, **kwargs):
    msg = flask_mail.Message(subject=\
            app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject, 
            sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = flask.render_template(template_file+'.txt', **kwargs)
    msg.html = flask.render_template(template_file+'.html', **kwargs)

    thread = threading.Thread(target=async_send, args=(msg,))
    thread.daemon = True
    thread.start()

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    # add foreign key
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<role {}>'.format(self.name)
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))

    # add foreign key
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<user {}>'.format(self.user_name)

class loginForm(flask_wtf.FlaskForm):
    name = wtforms.StringField('Input your name',
            validators = [validators.Required()])
    password = wtforms.PasswordField('Input your password',
            validators = [validators.Required()])
    submit = wtforms.SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = loginForm()
    if form.validate_on_submit():
        users = User.query.filter_by(user_name=form.name.data).all()
        if users:
            flask.session['known'] = True
        else:
            flask.session['known'] = False
            user = User(user_name=form.name.data, 
                    password=form.password.data)
            db.session.add(user)
            send_email(app.config['FLASKY_ADMIN'], 'New User',
                    'mail/new_user', user=user)
        flask.session['name'] = form.name.data
        form.name.data = ''
        return flask.redirect(flask.url_for('index'))
    return flask.render_template('index.html', 
            form = form, name=flask.session.get('name'),
            known = flask.session.get('known'))
@app.route('/user/<string:user_name>')
def user(user_name):
    return flask.render_template('user.html', user_name=user_name)
@app.errorhandler(404)      # error handler for 404 error
def page_not_found(error):
    # error is werkzeug.exceptions.NotFound, have code and description attr
    # i am not sure if not return error code is ok, but you should add it
    return flask.render_template('404.html'), 404
@app.errorhandler(500)
def internal_error(error):
    # error is werkzeug.exceptions.InternalServerError, have code and description attr
    return flask.render_template('500.html', 
            admin_email="liuty196888@gmail.com"), 500

manager.add_command('shell', flask_script.Shell(use_ipython=True, 
        make_context=lambda : \
                dict(app=app, User=User, Role=Role, db=db)))
if __name__ == '__main__':
    # app.run(debug=True)
    manager.run()
