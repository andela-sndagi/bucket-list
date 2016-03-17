# bucketlist/api.py

import app

app.app.config.from_object('bucketlist.config.DevelopmentConfig')

app.manager.run()
