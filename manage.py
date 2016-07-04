# !/usr/bin/env python
#  encoding: utf-8

'''
启动脚本
增加runserver命令可以在pycharm中运行调试
'''

import os
from app import create_app, db
from app.models import User, Role
from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
	return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)
manager.add_command("runserver", Server(use_debugger=True))


@manager.command
def test():
	'''Run the unit tests'''
	import unittest
	tests = unittest.TestLoader().discover('tests')
	unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == "__main__":
	manager.run()