import json
import os
import threading
from pathlib import Path

import gradio as gr
from assets.i18n.i18n import I18nAuto


i18n = I18nAuto()
config_file = Path(__file__).resolve().parents[3] / "assets" / "config.json"
AUTO_LANGUAGE = "Language automatically detected in the system"
LANGUAGE_CHOICES = [("English", "en_US"), ("简体中文", "zh_CN")]

# The backend restarts to rebuild all translated Gradio components. Wait for
# the new interface before reloading, rather than racing the server startup.
LANGUAGE_RELOAD_JS = """(language) => {
    if (typeof language !== 'string') return [language];
    const expectedTitle = language === 'Language automatically detected in the system'
        ? null : (language.startsWith('zh') ? 'AI唱歌克隆' : 'Murphy Voice Studio');
    setTimeout(async () => {
        for (let attempt = 0; attempt < 60; attempt++) {
            try {
                const response = await fetch(`./config?language_reload=${Date.now()}`, {cache: 'no-store'});
                if (response.ok && (expectedTitle === null || (await response.json()).title === expectedTitle)) {
                    window.location.reload();
                    return;
                }
            } catch (_) { /* Wait while the local server is restarting. */ }
            await new Promise(resolve => setTimeout(resolve, 1000));
        }
        window.location.reload();
    }, 2000);
    return [language];
}"""


def get_language_settings():
    with config_file.open(encoding="utf-8") as file:
        config = json.load(file)
    return config["lang"]["selected_lang"] if config["lang"]["override"] else AUTO_LANGUAGE


def save_lang_settings(selected_language, notify=True):
    if selected_language != AUTO_LANGUAGE and selected_language not in i18n._get_available_languages():
        raise gr.Error("Unknown language / 未知语言")
    with config_file.open(encoding="utf-8") as file:
        config = json.load(file)
    config["lang"]["override"] = selected_language != AUTO_LANGUAGE
    if selected_language != AUTO_LANGUAGE:
        config["lang"]["selected_lang"] = selected_language
    temporary = config_file.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, config_file)
    if notify:
        gr.Info(i18n("Language saved. Apply and restart to update the interface."))


def apply_language(selected_language):
    save_lang_settings(selected_language, notify=False)
    gr.Info(i18n("Applying language. The studio will restart and this page will reload."))
    from tabs.settings.sections.restart import restart_applio

    timer = threading.Timer(1.0, restart_applio)
    timer.daemon = True
    timer.start()


def language_switcher():
    with gr.Row(elem_id="language-toolbar"):
        selected_language = gr.Dropdown(
            label="Language / 语言",
            choices=LANGUAGE_CHOICES,
            value="zh_CN" if i18n.language.startswith("zh") else "en_US",
            interactive=True,
            min_width=170,
        )
        apply_button = gr.Button(i18n("Apply and restart"), elem_id="language-apply")
        apply_button.click(
            fn=apply_language,
            inputs=[selected_language],
            outputs=[],
            js=LANGUAGE_RELOAD_JS,
            api_name=False,
        )


def lang_tab():
    choices = [("Automatic / 跟随系统", AUTO_LANGUAGE)] + LANGUAGE_CHOICES
    choices += [(language, language) for language in sorted(i18n._get_available_languages())
                if language not in {"en_US", "zh_CN"}]
    with gr.Column():
        selected_language = gr.Dropdown(
            label="Language / 语言",
            info=i18n("Select the language you want to use. (Requires restarting Applio)"),
            value=get_language_settings(),
            choices=choices,
            interactive=True,
        )
        selected_language.change(fn=save_lang_settings, inputs=[selected_language], outputs=[])
        apply_button = gr.Button(i18n("Apply and restart"))
        apply_button.click(fn=apply_language, inputs=[selected_language], outputs=[],
                           js=LANGUAGE_RELOAD_JS, api_name=False)
