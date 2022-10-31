import json
from collections import Counter
from pathlib import Path

import arabic_reshaper
from bidi.algorithm import get_display
from hazm import Normalizer, word_tokenize
from loguru import logger
from src.data import DATA_DIR
from wordcloud import WordCloud


class ChatStatistics:
    def __init__(self, chat_data):
        self.normalizer = Normalizer()
        logger.info(f'loading data from {chat_data}')
        with open(chat_data) as f:
            self.chat_data = json.load(f)
        with open(DATA_DIR / 'text.txt') as d:
            self.stop_words = d.readlines()
            self.stop_words = list(map(str.strip, self.stop_words))
    
    def word_cloud(self, output_dir):
        logger.info('genrating your word cloud')
        text = ''
        for message in self.chat_data['messages']:
            if type(message['text']) is str and message['text'] != '':
                token = word_tokenize(message['text'])
                token = list(filter(lambda item: item not in self.stop_words, token))
                text += f" {' '.join(token)}"
        
        text = arabic_reshaper.reshape(text)
        text = get_display(text)
        text = arabic_reshaper.reshape(text)
        text = get_display(text)
        wordcloud = WordCloud(
            font_path=str(DATA_DIR / 'BHoma.ttf'),
            background_color='white',
            width=1200, height=1200
            ).generate(text)
        wordcloud.to_file(Path(output_dir) / 'wordcloud.jpg')
        print('DONE!')


if __name__ == '__main__':
    test_data = ChatStatistics(chat_data=DATA_DIR / 'familly_group.json')
    test_data.word_cloud(output_dir= DATA_DIR)
