import configparser, logging, telegram, os, json

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

config = configparser.ConfigParser()
config.read('config.ini') # 讀取設定檔

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def character_about_handler(update, context):
    keyboard = [[InlineKeyboardButton('滝川みう', callback_data='character miu')],
            [InlineKeyboardButton('斎藤ニコル', callback_data='character nicoru'),
            InlineKeyboardButton('河野都', callback_data='character miyako')],
            [InlineKeyboardButton('藤間桜', callback_data='character sakura'),
            InlineKeyboardButton('佐藤麗華', callback_data='character reika')],
            [InlineKeyboardButton('立川絢香', callback_data='character ayaka'),
            InlineKeyboardButton('戸田ジュン', callback_data='character jun')],
            [InlineKeyboardButton('丸山あかね', callback_data='character akane'),
            InlineKeyboardButton('神木みかみ', callback_data='character mikami')],
            [InlineKeyboardButton('東条悠希', callback_data='character yuki'),
            InlineKeyboardButton('柊つぼみ', callback_data='character tsubomi')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('角色個人資料', reply_markup=reply_markup)

def character_about_callback_handler(update, context):
    query = update.callback_query
    character_name = query.data.split()[1]
    with open('character_about.json', encoding='utf-8') as f:
        character_out = json.load(f)
        message_str = '姓名：' + str(character_out[character_name]['name']) + '\n' \
                            '年齡：' + str(character_out[character_name]['age']) + '\n' \
                            '生日：' + str(character_out[character_name]['brithday']) + '\n' \
                            '血型：' + str(character_out[character_name]['bloodgroup']) + '\n' \
                            '出身：' + str(character_out[character_name]['background']) + '\n' \
                            '應援色：' + str(character_out[character_name]['imagecolor']) + '\n' \
                            '座右銘：' + str(character_out[character_name]['motto']) + '\n' \
                            '特技：' + str(character_out[character_name]['specialty']) + '\n' \
                            '夢想：' + str(character_out[character_name]['dream']) + '\n' \
                            '喜愛的食物：' + str(character_out[character_name]['likefood']) + '\n' \
                            '不擅長的事物：' + str(character_out[character_name]['notgoodat']) + '\n' \
                            '興趣：' + str(character_out[character_name]['interest']) + '\n' \
                            '聲優：' + str(character_out[character_name]['seiyuu']) + '\n' \
                            '簡介：' + str(character_out[character_name]['introduction'])
        query.message.reply_text(message_str)

def seiyuu_about_handler(update, context):
    keyboard = [[InlineKeyboardButton('西條和', callback_data='seiyuu nagomi'),
            InlineKeyboardButton('花川芽衣', callback_data='seiyuu mei')],
            [InlineKeyboardButton('河瀬詩', callback_data='seiyuu uta'),
            InlineKeyboardButton('倉岡水巴', callback_data='seiyuu mizuwa')],
            [InlineKeyboardButton('天城サリー', callback_data='seiyuu sally'),
            InlineKeyboardButton('帆風千春', callback_data='seiyuu chiharu')],
            [InlineKeyboardButton('宮瀬玲奈', callback_data='seiyuu reina'),
            InlineKeyboardButton('海乃るり', callback_data='seiyuu ruri')],
            [InlineKeyboardButton('白沢かなえ', callback_data='seiyuu kanae'),
            InlineKeyboardButton('涼花萌', callback_data='seiyuu moe')],
            [InlineKeyboardButton('高辻麗', callback_data='seiyuu urara'),
            InlineKeyboardButton('武田愛奈', callback_data='seiyuu aina')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('聲優個人資料', reply_markup=reply_markup)

def seiyuu_about_callback_handler(update, context):
    query = update.callback_query
    seiyuu_name = query.data.split()[1]
    with open('seiyuu_about.json', encoding='utf-8') as f:
        seiyuu_out = json.load(f)
        message_str = '姓名：' + str(seiyuu_out[seiyuu_name]['name']) + '\n' \
                        '生日：' + str(seiyuu_out[seiyuu_name]['brithday']) + '\n' \
                        '血型：' + str(seiyuu_out[seiyuu_name]['bloodgroup']) + '\n' \
                        '身高：' + str(seiyuu_out[seiyuu_name]['height']) + '\n' \
                        '出身：' + str(seiyuu_out[seiyuu_name]['background'])
        query.message.reply_text(message_str)

def project_about_handler(update, context):
    update.message.reply_text('22/7這個企劃是由秋元康、Sony Music以及Aniplex合作組成的2.5次元聲優偶像。在2016年發表此企劃，並在12/24日選出12位入選者(1人後來退出)，22/7是π的近似值(代表著從0中產生1的時候，對不存在的事物、尚未見到的事物的相信之力是必要的。22/7是想像的象徵。究竟有甚麼含義呢？未來就在未來)。')

if __name__ == '__main__':
    token = config['TELEGRAM']['ACCESS_TOKEN']
    updater = Updater(token , use_context=True)
    PORT = int(os.environ.get('PORT', '5000'))
    dp = updater.dispatcher
    dp.add_handler(CallbackQueryHandler(character_about_callback_handler, pattern='^character'))
    dp.add_handler(CommandHandler('character', character_about_handler))
    dp.add_handler(CallbackQueryHandler(seiyuu_about_callback_handler, pattern='^seiyuu'))
    dp.add_handler(CommandHandler('seiyuu', seiyuu_about_handler))
    dp.add_handler(CommandHandler('project', project_about_handler))

    updater.start_webhook(listen='0.0.0.0',port=PORT, url_path=token)
    updater.bot.set_webhook("https://nanaonbot.herokuapp.com/" + token)

    updater.idle()