import os
import logging

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

texts = []
labels = []

PORT = int(os.environ.get('PORT', '8443'))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

with open('dataset.txt', 'r') as f:
    for line in f.readlines():
        label, text = line.strip().split(' ', 1)
        texts.append(text)
        labels.append(int(label != '__label__NORMAL'))

len(texts)
len(labels)

texts[:3]
labels[:3]

X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=1)

X_train[:3]

cv = CountVectorizer()
cv.fit(X_train[:3])

cv.vocabulary_
cv.transform(['братан наверно за клумбой наверно']).toarray()
cv.transform(['братан наверно за клумбой наверно бифуркация']).toarray()

model = make_pipeline(CountVectorizer(min_df=5), LogisticRegression(max_iter=3000))
model.fit(X_train, y_train)
model.predict(['привет', 'иди в задницу'])
model.predict_proba(['привет', 'иди в задницу'])
model.steps[1][1].coef_
model.steps[1][1].coef_.shape

TOKEN = os.environ.get('TOKEN', None)

print(TOKEN)


def reply(text):
    if not text:
        return 'Текст пустой'
    proba = model.predict_proba([text])[0, 1]
    return f'Текст "{text}" - токсичный на {proba:2.2%}'


print(reply('иди на хер'))
print(classification_report(y_test, model.predict(X_test)))
print(roc_auc_score(y_test, model.predict_proba(X_test)[:, 1]))


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text(
        "Привет! Я чат-бот, умею определять токсичность текста, который Вы мне пришлете. Оправьте любой текст ответным сообщением.")


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text(
        "Привет! Я чат-бот, умею определять токсичность текста, который Вы мне пришлете. Оправьте любой текст ответным сообщением.")


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(reply(update.message.text))


def main():
    """Start the bot."""
    APP_NAME = 'https://project-2-tgbot-toxicity-class.herokuapp.com/'

    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # #Start the Bot
    # updater.start_webhook(
    #     listen="0.0.0.0",
    #     port=int(PORT),
    #     url_path=TOKEN,
    #     webhook_url=APP_NAME + TOKEN
    # )
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()