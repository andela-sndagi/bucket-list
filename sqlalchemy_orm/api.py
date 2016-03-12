# sqlalchemy_orm/api.py

import app

app.app.config.from_object('sqlalchemy_orm.config.DevelopmentConfig')

app.manager.run()
