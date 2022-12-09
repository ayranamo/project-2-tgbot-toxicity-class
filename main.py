import os
import logging

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Токен берем из переменной окружения
TOKEN = os.environ.get('TOKEN')

# Включение логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Создаем массивы
texts = []
labels = []

# Загружаем данные
with open('dataset.txt', 'r') as f:
    for line in f.readlines():
        label, text = line.strip().split(' ', 1)
        texts.append(text)
        labels.append(int(label != '__label__NORMAL'))

# Разбиваем данные на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=1)

X_train[:3]

cv = CountVectorizer()
cv.fit(X_train[:3])

cv.vocabulary_
cv.transform(['братан наверно за клумбой наверно']).toarray()
cv.transform(['братан наверно за клумбой наверно бифуркация']).toarray()

# Cоздадим связку из двух моделей - CountVectorizer и LogisticRegression. Они будут обучаться, как единая модель.
model = make_pipeline(CountVectorizer(min_df=5), LogisticRegression(max_iter=3000))
model.fit(X_train, y_train)

# Протестируем обученную систему. Для первого текста она предсказывает 0 ("нормальный"), для второго - 1 ("токсичный").
model.predict(['привет', 'иди в задницу'])

# Посмотрим на вероятности
model.predict_proba(['привет', 'иди в задницу'])
model.steps[1][1].coef_
model.steps[1][1].coef_.shape

# Определяем функцию, которая будет оценивать степень токсичности текста
def reply(text):
    if not text:
        return 'Текст пустой'
    proba = model.predict_proba([text])[0, 1]
    return f'Текст "{text}" - токсичный на {proba:2.2%}'

print(reply('иди на хер'))

# В sklearn есть функция classification_report, которая выводит точность и полноту для каждого класса и в среднем.
print(classification_report(y_test, model.predict(X_test)))
print(roc_auc_score(y_test, model.predict_proba(X_test)[:, 1]))

# Выводит приветствие
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text(
        "Привет! Я чат-бот, умею определять токсичность текста, который Вы мне пришлете. Оправьте любой текст ответным сообщением.")

# Выводит подсказку
def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text(
        "Привет! Я чат-бот, умею определять токсичность текста, который Вы мне пришлете. Оправьте любой текст ответным сообщением.")

# Отвечает на любое сообщение
def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(reply(update.message.text))

def main():
    # Создаем Updater и передаем ему токен бота. Токен бота берем из переменной окружения.
    updater = Updater(TOKEN, use_context=True)

    # Регистрируем обработчики
    dp = updater.dispatcher

    # Регистрируем команды
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # Регистрируем обработчик сообщений
    dp.add_handler(MessageHandler(Filters.text, echo))

    # Запускаем бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
