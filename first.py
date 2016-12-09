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

@app.route('/<string:name>')
def index(name):
    return flask.render_template('user.html', name=name)
@app.errorhandler(404)      # error handler for 404 error
def page_not_found(error):
    # error is werkzeug.exceptions.NotFound, have code and description attr
    return flask.render_template('404.html')
@app.errorhandler(500)
def internal_error(error):
    # error is werkzeug.exceptions.InternalServerError, have code and description attr
    return flask.render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
