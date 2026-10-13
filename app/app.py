# Plataform config
from rvc.lib.platform import platform_config

platform_config()

import gradio as gr
import sys
import os
import pathlib
import logging
import inspect

from typing import Any
from assets.brand import get_app_name, get_brand_html, load_brand_css
from tabs.settings.sections.lang import language_switcher

DEFAULT_SERVER_NAME = "127.0.0.1"
DEFAULT_PORT = 6969
MAX_PORT_ATTEMPTS = 10

# Set up logging
logging.getLogger("uvicorn").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)

# Add current directory to sys.path
now_dir = os.getcwd()
sys.path.append(now_dir)

# Zluda hijack
import rvc.lib.zluda

# Import Tabs
from tabs.inference.inference import inference_tab
from tabs.train.train import train_tab
from tabs.extra.extra import extra_tab
from tabs.report.report import report_tab
from tabs.download.download import download_tab
from tabs.tts.tts import tts_tab
from tabs.voice_blender.voice_blender import voice_blender_tab
from tabs.plugins.plugins import plugins_tab
from tabs.settings.settings import settings_tab
from tabs.realtime.realtime import realtime_tab

# Run prerequisites
from core import run_prerequisites_script

run_prerequisites_script(
    pretraineds_hifigan=True,
    models=True,
    exe=True,
)

# Initialize i18n
from assets.i18n.i18n import I18nAuto

i18n = I18nAuto()
APP_NAME = get_app_name(i18n.language)
HEADER_HTML, WORKFLOW_HTML, FOOTER_HTML = get_brand_html(i18n.language)

# Start Discord presence if enabled
from tabs.settings.sections.presence import load_config_presence

if load_config_presence():
    from assets.discord_presence import RPCManager

    RPCManager.start_presence()

# Check installation
import assets.installation_checker as installation_checker

installation_checker.check_installation()

# Load theme
import assets.themes.loadThemes as loadThemes

my_applio = loadThemes.load_theme() or "ParityError/Interstellar"
client_mode = "--client" in sys.argv

# Gradio 5 configures appearance in Blocks; Gradio 6 configures it in launch.
ui_options = {
    "theme": my_applio,
    "css": load_brand_css(i18n.language),
    "js": (
        pathlib.Path("tabs/realtime/main.js").read_text(encoding="utf-8")
        if client_mode
        else None
    ),
}
ui_options_in_launch = "theme" in inspect.signature(gr.Blocks.launch).parameters

# Define Gradio interface
with gr.Blocks(
    title=APP_NAME,
    **({} if ui_options_in_launch else ui_options),
) as Applio:
    language_switcher()
    gr.HTML(HEADER_HTML, elem_id="brand-header")
    with gr.Tabs(elem_id="main-tabs"):
        with gr.Tab(i18n("Inference")):
            gr.HTML(WORKFLOW_HTML, elem_id="workflow-guide")
            inference_tab()

        with gr.Tab(i18n("Training")):
            train_tab()

        with gr.Tab(i18n("TTS")):
            tts_tab()

        with gr.Tab(i18n("Voice Blender")):
            voice_blender_tab()

        with gr.Tab(i18n("Realtime")):
            realtime_tab()

        with gr.Tab(i18n("Plugins")):
            plugins_tab()

        with gr.Tab(i18n("Download")):
            download_tab()

        with gr.Tab(i18n("Report a Bug")):
            report_tab()

        with gr.Tab(i18n("Extra")):
            extra_tab()

        with gr.Tab(i18n("Settings")):
            settings_tab()

    gr.HTML(FOOTER_HTML, elem_id="brand-footer")


def launch_gradio(server_name: str, server_port: int) -> None:
    app, _, _ = Applio.launch(
        favicon_path="assets/ICON.ico",
        share="--share" in sys.argv,
        inbrowser="--open" in sys.argv,
        server_name=server_name,
        server_port=server_port,
        prevent_thread_lock=client_mode,
        **(ui_options if ui_options_in_launch else {}),
    )

    if client_mode:
        import time
        from rvc.realtime.client import app as fastapi_app

        app.mount("/api", fastapi_app)

        while True:
            time.sleep(5)


def get_value_from_args(key: str, default: Any = None) -> Any:
    if key in sys.argv:
        index = sys.argv.index(key) + 1
        if index < len(sys.argv):
            return sys.argv[index]
    return default


if __name__ == "__main__":
    port = int(get_value_from_args("--port", DEFAULT_PORT))
    server = get_value_from_args("--server-name", DEFAULT_SERVER_NAME)

    for _ in range(MAX_PORT_ATTEMPTS):
        try:
            launch_gradio(server, port)
            break
        except OSError:
            print(
                f"Failed to launch on port {port}, trying again on port {port - 1}..."
            )
            port -= 1
        except Exception as error:
            print(f"An error occurred launching Gradio: {error}")
            break
