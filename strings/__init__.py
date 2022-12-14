import sys
import os
from typing import Any, Dict, List, Union
from glob import glob
from pyUltroid import *
from pyUltroid.functions.tools import translate
try:
    from yaml import safe_load
except ModuleNotFoundError:
    from pyUltroid.functions.tools import safe_load

language = [udB.get_key("language") or os.getenv("LANGUAGE") or "en"]
languages = {}

for file in glob("strings/strings/*yml"):
    if file.endswith(".yml"):
        code = file.split("/")[-1].split("\\")[-1][:-4]
        try:
            languages[code] = safe_load(
                open(file, encoding="UTF-8"),
            )
        except Exception as er:
            LOGS.info(f"Error in {file[:-4]} language file")
            LOGS.exception(er)


def get_string(key: str) -> Any:
    lang = language[0]
    try:
        return languages[lang][key]
    except KeyError:
        try:
            en_ = languages["en"][key]
            tr = translate(en_, lang_tgt=lang).replace("\ N", "\n")
            if en_.count("{}") != tr.count("{}"):
                tr = en_
            if languages.get(lang):
                languages[lang][key] = tr
            else:
                languages.update({lang: {key: tr}})
            return tr
        except KeyError:
            return f"Warning: could not load any string with the key `{key}`"
        except TypeError:
            pass
        except Exception as er:
            LOGS.exception(er)
        return languages["en"].get(key) or f"Failed to load language string '{key}'"

def get_help(key):
    doc = get_string(key)
    if doc:
        return get_string("cmda") + doc

def get_languages() -> Dict[str, Union[str, List[str]]]:
    return {
        code: {
            "name": languages[code]["name"],
            "natively": languages[code]["natively"],
            "authors": languages[code]["authors"],
        }
        for code in languages
    }
