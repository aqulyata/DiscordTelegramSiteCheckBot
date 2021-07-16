import speedtest
from discord_site_check_bot.command.base.Command import Command


class SpeedCommand(Command):
    def execute(self, message, bot):
        threads = None
        s = speedtest.Speedtest()
        download = round(s.download(threads=threads) % 1024 % 1024)
        upload = round(s.upload(threads=threads) % 1024 % 1024)
        bot.send_message(message.chat.id, 'Speed of download:' + str(download) + ' ' + 'Mbites\s')
        bot.send_message(message.chat.id, 'Speed of upload:' + str(upload) + ' ' + 'Mbite\s')

    def get_name(self):
        return 'speed'
