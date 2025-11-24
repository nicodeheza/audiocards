# Export Card to Audio (Anki Add-on)

This is an [Anki](https://apps.ankiweb.net/) add-on that allows you to convert your notes to an .mp3 file so you can listen to your card content.

You can select your recognition and recall fields to add them to the audio. If the field has audio, the audio will be used; if it has text, the add-on will convert the text to speech.

Currently, the add-on **only works on Windows**. If you are a developer and want to add support for another OS, contributions are more than welcome.

## Installation

You can install it directly through the regular Anki add-on installation process. Here is the [add-on link](https://ankiweb.net/shared/info/1117983796).

To install it through GitHub, clone this repo to your Anki add-on directory. Then:

```powershell
cd audiocards

pip install -r requirements.txt -t ./lib
```

## How to use it

1. In Anki click on browser.
2. Right-click on one card or select a bunch of cards and right-click.
3. On the menu, click > "Export audio card/s"
4. Complete all the fields and click on accept.

### Fields

- **Card Front Field**: The field that has the front information of your card.
- **Card Back Field**: The field that has the back information of your card.
- **Front language** : The language of the field; this is only important if your field has text data.
- **Back language** : The language of the field; this is only important if your field has text data.
- **Delay time in s** : How many seconds of silence to add between each field audio.
- **Audio pattern** : Define the order and the amount of time each field audio is played. E.g.: "ffbb" will play the front audio two times and then the back audio two times. Only accepts "f" and "b" characters.
- **Add a beep at the beginning** : If checked, a beep will be added at the beginning of the audio file.
- **Save Directory** : The directory where the files are going to be saved.
