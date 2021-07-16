import io
import matplotlib.pyplot as plt
#from openpyxl.drawing.image import Image
#import speedtest
from discord_site_check_bot.command.base.Command import Command


class GraphicsCommand(Command):
    def execute(self, message, bot):
        x = [8, 9]
        y1 = [7, 5]
        y2 = [4, 10]
        plt.figure(figsize=(20, 15))
        plt.plot(x, y1, 'o-r', alpha=0.7, label="download", lw=5, mec='b', mew=2, ms=10)
        plt.plot(x, y2, 'v-.g', label="upload", mec='r', lw=2, mew=2, ms=12)
        plt.legend()
        plt.grid(True)
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        bot.send_photo(message.chat.id, buf)

    def get_name(self):
        return 'graphics'
