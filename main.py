from PIL import Image
import time
import telepot
import telepot.namedtuple
from telepot.loop import MessageLoop
import config


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    m = telepot.namedtuple.Message(**msg)
    print(msg)

    if chat_id < 0:
        # group message
        print('Received a %s from %s, by %s' % (content_type, m.chat, m.from_))
    else:
        # private message
        print('Received a %s from %s' % (content_type, m.chat))  # m.chat == m.from_

    if content_type == 'sticker':
        reply = ''
        sticker = msg['sticker']['file_id'] + '.webp'
        bot.download_file(msg['sticker']['file_id'], dest=sticker)
        a = Image.open(sticker)
        a.save((sticker[:-4] + '.png'))
        bot.sendDocument(chat_id, open((sticker[:-4] + '.png'), 'rb'))

    if content_type == 'text':
        reply = ''

        # For long messages, only return the first 10 characters.
        if len(msg['text']) > 10:
            reply = u'First 10 characters:\n'

        reply += msg['text'][:10].encode('unicode-escape').decode('ascii')
        bot.sendMessage(chat_id, reply)


bot = telepot.Bot(config.TOKEN)
MessageLoop(bot, handle).run_as_thread()
print('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)
