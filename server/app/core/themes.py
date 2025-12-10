import os
import configparser
from jinja2 import Environment, FileSystemLoader

# Paths
# Assumes structure: server/app/core/themes.py -> server/
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
STYLES_DIR = os.path.join(BASE_DIR, "styles")
# Point to the actual template files which seem to be nested in 'author'
TEMPLATE_DIR = os.path.join(BASE_DIR, "template", "author")

# Global storage
THEMES = {}
JINJA_ENV = None

def load_themes():
    global JINJA_ENV
    
    # Initialize Jinja2 Env
    if os.path.exists(TEMPLATE_DIR):
        JINJA_ENV = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    else:
        print(f"Warning: Template dir not found at {TEMPLATE_DIR}")

    # Load INI files
    if not os.path.exists(STYLES_DIR):
        print(f"Warning: Styles dir not found at {STYLES_DIR}")
        return

    print(f"Loading themes from {STYLES_DIR}...")
    count = 0
    for root, _, files in os.walk(STYLES_DIR):
        for file in files:
            if file.endswith(".ini"):
                file_path = os.path.join(root, file)
                theme_id = os.path.splitext(file)[0]
                
                try:
                    config = configparser.ConfigParser()
                    config.read(file_path, encoding='utf-8')
                    
                    if config.has_section('style'):
                        style_data = dict(config.items('style'))
                        THEMES[theme_id] = style_data
                        count += 1
                except Exception as e:
                    print(f"Error loading theme {file}: {e}")
    
    print(f"Loaded {count} themes.")

def get_theme(theme_id: str):
    return THEMES.get(theme_id)

def get_all_themes():
    return sorted(list(THEMES.keys()))

def get_jinja_env():
    if JINJA_ENV is None:
        load_themes()
    return JINJA_ENV
