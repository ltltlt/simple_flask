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

app = flask.Flask(__name__)
bootstrap = flask_bootstrap.Bootstrap(app)
manager = flask_script.Manager(app)

@app.route('/<string:user_name>')
def index(user_name):
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

if __name__ == '__main__':
    # app.run(debug=True)
    manager.run()
