from . import utils

utils.importLocalDependency("gtts")

from gtts import lang, gTTS


def getLanguages():
    langs = []
    langs_map = lang.tts_langs()
    for l in langs_map:
        langs.append(langs_map[l])
    return langs


def getLangMap():
    original_lang_map = lang.tts_langs()
    return {v: k for k, v in original_lang_map.items()}


def textToSpeech(text: str, lang: str, file_name: str):
    obj = gTTS(text=text, lang=lang, slow=False)
    obj.save(file_name)
