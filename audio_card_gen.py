from . import ffmpeg, my_dialog
from aqt import mw, qt
from . import utils, text_to_speech
import uuid
from os.path import dirname


def onExportAudioCardSelected(browser):
    if not mw or not mw.addonManager or not mw.col:
        return
    dialog = my_dialog.MyDialog(browser)
    if dialog.exec():

        front_field = dialog.front_combo.itemText(dialog.front_combo.currentIndex())
        back_field = dialog.back_combo.itemText(dialog.back_combo.currentIndex())
        front_lang_label = dialog.front_lang_combo.itemText(
            dialog.front_lang_combo.currentIndex()
        )
        back_lang_label = dialog.back_lang_combo.itemText(
            dialog.back_lang_combo.currentIndex()
        )

        lang_map = text_to_speech.getLangMap()
        front_lang = lang_map[front_lang_label]
        back_lang = lang_map[back_lang_label]

        delay_field = dialog.delay_input.text()
        pattern_filed = dialog.pattern_input.text()
        is_bip_active = dialog.add_bip_checkbox.isChecked()
        directory_field = dialog.directory_input.text()

        config = mw.addonManager.getConfig(__name__)
        config = config if config else {}
        config["last_front_field"] = front_field
        config["last_back_field"] = back_field
        config["last_front_lang_field"] = front_lang_label
        config["last_back_lang_field"] = back_lang_label
        config["delay"] = delay_field
        config["pattern"] = pattern_filed
        config["add_bip"] = "true" if is_bip_active else "false"
        config["directory"] = directory_field
        mw.addonManager.writeConfig(__name__, config)

        progress_window = qt.QWidget()
        progress_window.setWindowTitle("Generating Audio Cards")
        progress_window.setFixedSize(400, 80)

        progress_text = qt.QLabel("Processing...")
        progress_layout = qt.QVBoxLayout()
        progress_layout.addWidget(progress_text)

        progress_window.setLayout(progress_layout)
        progress_window.show()
        progress_window.setFocus()

        progress_text.setText(f"0 of {len(dialog.selected_notes)} done")
        mw.app.processEvents()
        mw.app.processEvents()

        processed = 0
        for note_id in dialog.selected_notes:
            if not progress_window.isVisible():
                return
            note = mw.col.get_note(note_id)
            front = note[front_field]
            back = note[back_field]
            front_files = getFieldAudioFile(front, front_lang)
            back_files = getFieldAudioFile(back, back_lang)
            ffmpeg.concat_audio(
                front_files=front_files,
                back_files=back_files,
                silence_duration=int(delay_field),
                add_bip=is_bip_active,
                pattern=pattern_filed,
                output_file=f"{directory_field}/{note_id}.mp3",
            )

            for front_file in front_files:
                if "temp_" in front_file:
                    utils.removeFile(front_file)
            for back_file in back_files:
                if "temp_" in back_file:
                    utils.removeFile(back_file)
            processed += 1
            progress_text.setText(f"{processed} of {len(dialog.selected_notes)} done")
            mw.app.processEvents()


def getFieldAudioFile(filed: str, lang: str) -> list[str]:
    if not mw or not mw.col:
        return []
    if "sound:" in filed:
        files_names = get_files_list(filed)
        res: list[str] = []
        for file_name in files_names:
            if ".mp3" in file_name:
                res.append(mw.col.media.dir() + f"\\{file_name}")
                continue
            new_file_name = f"{dirname(__file__)}\\temp_{uuid.uuid4()}.mp3"
            ffmpeg.convertToMp3(mw.col.media.dir() + f"\\{file_name}", new_file_name)
            res.append(new_file_name)
        return res

    clean_text = utils.cleanFieldText(filed)
    file_name = f"{dirname(__file__)}\\temp_{uuid.uuid4()}.mp3"
    text_to_speech.textToSpeech(clean_text, lang, file_name)
    return [file_name]


def get_files_list(filed: str) -> list[str]:
    res = filed.replace("sound:", "").replace("[", "").split("]")
    return res[:-1]
