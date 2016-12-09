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

# type:name, the name must the same as function argument,
# for it will pass as keyword argument
@app.route('/str/<string:path>')        # string accept any char except /
def index(path):
    return "<b>{}</b>".format(path)
@app.route('/float/<float:num>')    # float accept [0-9]*\.[0-9]*
def flo(num):
    return "<b>{}</b>".format(num)
@app.route('/int/<int:num>')    # int accept [0-9]*
def intt(num):
    return "<b>{}</b>".format(num)
@app.route('/path/<path:pathname>') # path accept any str including /
def path(pathname):
    flask.make_response()
    return "<b>{}</b>".format(pathname)

if __name__ == '__main__':
    manager.run()
    # app.run(debug=True)
