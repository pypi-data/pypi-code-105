#! /usr/bin/env python
from os import path as p
from appdirs import user_data_dir, user_config_dir
from configparser import ConfigParser as conf
from pydub import AudioSegment as audio
from pydub.playback import play

data_dir = user_data_dir("Quran")
cfg_dir = user_config_dir()
cfg = conf()
config_file = f"{cfg_dir}/quran-rofi.ini"

if not p.isfile(config_file):
    cfg.add_section("Font")
    cfg.set("Font", "font", "Al Qalam Quran Majeed 20")

    cfg.add_section("Murotal")
    cfg.set("Murotal", "qori", "Saad Al-Gamdi")
    cfg.set("Murotal", "autoplay", "off")
    
    with open(config_file, "w") as cfg_ini:
        cfg.write(cfg_ini)
else:
    cfg.read(config_file)

autoplay = cfg["Murotal"]["autoplay"]

def Murotal(id_surat, id_ayat):
    id_surat = str(id_surat)
    id_ayat = str(id_ayat)
    if len(id_surat) == 2:
        surat = f"0{id_surat}"
    elif len(id_surat) == 3:
        surat = f"{id_surat}"
    else:
        surat = f"00{id_surat}"
     
    if len(id_ayat) == 2:
        ayat = f"0{id_ayat}"
    elif len(id_ayat) == 3:
        ayat = f"{id_ayat}"
    else:
        ayat = f"00{id_ayat}"

    qori = cfg["Murotal"]["qori"] 
    murotal = f"{data_dir}/murotal/{qori}/{surat}{ayat}.mp3"
    murotal = audio.from_mp3(murotal)
    play(murotal)


def Theme(p):
    font_quran = cfg["Font"]["font"]
    th_ayat = 'inputbar {children: [prompt];} textbox {font : ' '"' + font_quran + '"' ';} listview {lines: 1; columns: 6;} element-text {horizontal-align: 0.5;}' 
    th_tafsir = 'inputbar {children: [prompt];} listview {lines: 1; columns: 3;} element-text {horizontal-align: 0.5;}'
    th_terjemahan = 'inputbar {children: [prompt];} listview {lines: 1; columns: 3;} element-text {horizontal-align: 0.5;}'
    if p >= 1000:
        th_ayat = 'inputbar {children: [prompt];} textbox {font : ' '"' + font_quran + '"' ';} listview {lines: 1; columns: 6;} element-text {horizontal-align: 0.5;} window {width: 95%;}'
    if p >= 1850:
        th_tafsir = 'inputbar {children: [prompt];} listview {lines: 1; columns: 3;} element-text {horizontal-align: 0.5;} window {width: 95%;}'
    return th_ayat, th_terjemahan, th_tafsir
