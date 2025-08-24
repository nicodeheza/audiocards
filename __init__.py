from aqt import browser, gui_hooks, qt
from . import audio_card_gen


def on_browser_will_show_context_menu(browser: browser.browser.Browser, menu: qt.QMenu):
    menu.addSeparator()
    menu.addAction(
        "Export audio card/s", lambda: audio_card_gen.onExportAudioCardSelected(browser)
    )


gui_hooks.browser_will_show_context_menu.append(on_browser_will_show_context_menu)
