# -*- coding: utf-8 -*-

from googletrans import Translator


text="測試"

translator = Translator()
result = translator.translate(text, dest='en').text
print(result)