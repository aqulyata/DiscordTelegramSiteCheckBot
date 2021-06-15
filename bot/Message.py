import datetime


class Message:

    def __init__(self, download, upload):
        self.download = download
        self.upload = upload
        self.date = datetime.datetime.now()
