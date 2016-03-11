import app

# configure to development
app.app.config.update(
    DEBUG=True, DATABASE_URI='sqlite://bucketlists.db')

app.manager.run()
