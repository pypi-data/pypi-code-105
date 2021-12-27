#! /usr/bin/env python

from alquran_id import AlQuran as Quran
from alquran_id.surat import *
from .config import *
from pyrof.rofi import Rofi
import subprocess as sub
from threading import Thread as thr

class quranRofi:
    def __init__(self):
        self.quran = Quran()

    def surat(self):
        th = 'listview {lines: 11; columns: 2;} window {width: 900px; border-radius: 6px;}'
        menu = Rofi(dpi=1, theme_str=th)
        menu.case_insensitive = True
        menu.prompt = "Al Quran"
        menu = menu(idSurat)
        id_surat = menu.value
        nama_surat = menu.selected
        return id_surat, nama_surat

    def idAyat(self):
        surat = self.surat()
        id_surat = surat[0]
        nama_surat = surat[1]
        jml_ayat = self.quran.JumlahAyat(id_surat)
        list_ayat = []
        for i in range(1, jml_ayat + 1):
            i = str(i)
            list_ayat.append(i)
        th = 'listview {lines: 3; columns: 11;} element-text {horizontal-align: 0.5;} window {width: 650px; border-radius: 6px;}'
        menu = Rofi(dpi=1, theme_str=th)
        menu.prompt = nama_surat
        menu = menu(list_ayat)
        id_ayat = menu.selected
        return nama_surat, id_surat, id_ayat, jml_ayat

    def getayat(self):
        quran = self.idAyat()
        nama_surat = quran[0]
        id_surat = quran[1]
        id_ayat = quran[2]
        jml_ayat = quran[3]
        ayat = self.quran.Ayat(id_surat, id_ayat)
        terjemahan = self.quran.Terjemahan(id_surat, id_ayat)
        tafsir = self.quran.Tafsir(id_surat, id_ayat)
        return nama_surat, id_surat, jml_ayat, id_ayat, ayat, terjemahan, tafsir

class showSurat:
    def __init__(self):
        self.quran = Quran()
        quran_rofi = quranRofi()
        Ayat = quran_rofi.getayat()
        self.nama_surat = Ayat[0]
        self.id_surat = Ayat[1]
        self.jml_ayat = Ayat[2]
        self.id_ayat = Ayat[3]
        self.terjemahan = Ayat[5]
        self.tafsir = Ayat[6]
        self.ayat = Ayat[4]
    
    def showRofi(self, theme, text, prompt, opt):
        menu = Rofi(dpi=1, theme_str=theme)
        menu.prompt = prompt
        menu.mesg = text
        menu = menu(opt)
        menu = menu.selected
        return menu
        
    def playMurotal(self):
        Murotal(self.id_surat, self.id_ayat)
    
    def showAyat(self):
        th = Theme(len(self.ayat))
        th = th[0]
        opt_ayat = ("Next", "Prev", "Terjemahan",  "Tafsir", "Surat", "Play")
        show = self.showRofi(th, f"\n{self.ayat}\n", f"{self.nama_surat} ayat {self.id_ayat}:", opt_ayat)
        if show == opt_ayat[0]:
            self.nextAyat()
        elif show == opt_ayat[1]:
            self.prevAyat()
        elif show == opt_ayat[2]:
            self.showTerjemahan()
        elif show == opt_ayat[3]:
            self.showTafsir()
        elif show == opt_ayat[4]:
            self.__init__()
            if autoplay == "on":
                thr(target=self.playMurotal).start()
                thr(target=self.showAyat).start()
            else:
                self.showAyat()
        elif show == opt_ayat[5]:
            thr(target=self.playMurotal).start()
            thr(target=self.showAyat).start()
    
    def showTerjemahan(self):
        th = Theme(len(self.terjemahan))
        th = th[1]
        opt_terjemahan = ("Back", "Copy")
        show = self.showRofi(th, f"{self.terjemahan}", f"Terjemahan {self.nama_surat} ayat {self.id_ayat}:", opt_terjemahan)
        if show == opt_terjemahan[0]:
            self.showAyat()
        elif show == opt_terjemahan[1]:
            self.copy()
    
    def showTafsir(self):
        th = Theme(len(self.tafsir))
        th = th[2]
        opt_tafsir = ("Back", "Copy")
        show = self.showRofi(th, f"{self.tafsir}", f"Tafsir {self.nama_surat} ayat {self.id_ayat}:", opt_tafsir)
        if show == opt_tafsir[0]:
            self.showAyat()
        elif show == opt_tafsir[1]:
            self.copy()
        print(len(self.tafsir))

    def nextAyat(self):
        self.id_ayat = int(self.id_ayat) + 1
        jml_ayt = self.quran.JumlahAyat(self.id_surat)
        if self.id_surat == "114" and self.id_ayat == jml_ayt + 1:
            self.__init__()
            if autoplay == "on":
                thr(target=self.playMurotal).start()
                thr(target=self.showAyat).start()
            else:
                self.showAyat()
        elif self.id_ayat == jml_ayt + 1:
            self.id_surat = int(self.id_surat) + 1
            self.id_ayat = 1
            self.nama_surat = list(idSurat).index(self.nama_surat)
            self.nama_surat = self.nama_surat + 1
            self.nama_surat = list(idSurat)[self.nama_surat]
            self.ayat = self.quran.Ayat(self.id_surat, self.id_ayat)
            self.terjemahan = self.quran.Terjemahan(self.id_surat, self. id_ayat)
            self.tafsir = self.quran.Tafsir(self.id_surat, 1)
            if autoplay == "on":
                thr(target=self.playMurotal).start()
                thr(target=self.showAyat).start()
            else:
                self.showAyat()
        else:
            self.ayat = self.quran.Ayat(self.id_surat, self.id_ayat)
            self.terjemahan = self.quran.Terjemahan(self.id_surat, self.id_ayat)
            self.tafsir = self.quran.Tafsir(self.id_surat, self.id_ayat)
            if autoplay == "on":
                thr(target=self.playMurotal).start()
                thr(target=self.showAyat).start()
            else:
                self.showAyat()

    def prevAyat(self):
        self.id_ayat = int(self.id_ayat) - 1
        self.id_surat = int(self.id_surat)
        if self.id_surat == 1 and self.id_ayat == 0:
            self.__init__()
            if autoplay == "on":
                thr(target=self.playMurotal).start()
                thr(target=self.showAyat).start()
            else:
                self.showAyat()
        elif self.id_ayat == 0:
            self.id_surat = int(self.id_surat) - 1
            self.id_ayat = self.quran.JumlahAyat(self.id_surat)
            self.nama_surat = list(idSurat).index(self.nama_surat)
            self.nama_surat = self.nama_surat - 1
            self.nama_surat = list(idSurat)[self.nama_surat]
            self.ayat = self.quran.Ayat(self.id_surat, self.id_ayat)
            self.terjemahan = self.quran.Terjemahan(self.id_surat, self.id_ayat)
            self.tafsir = self.quran.Tafsir(self.id_surat, self.id_ayat)
            if autoplay == "on":
                thr(target=self.playMurotal).start()
                thr(target=self.showAyat).start()
            else:
                self.showAyat()
        else:
            self.ayat = self.quran.Ayat(self.id_surat, self.id_ayat)
            self.terjemahan = self.quran.Terjemahan(self.id_surat, self.id_ayat)
            self.tafsir = self.quran.Tafsir(self.id_surat, self.id_ayat)
            if autoplay == "on":
                thr(target=self.playMurotal).start()
                thr(target=self.showAyat).start()
            else:
                self.showAyat()

    def copy(self):
        quran_text = f"Surat {self.nama_surat} Ayat {self.id_ayat} : \n {self.ayat} \n Terjemahan: \n {self.terjemahan} \n Tafsir: \n {self.tafsir}"
        copy_quran = sub.Popen(['xclip', '-selection', 'clipboard'], stdin=sub.PIPE, close_fds=True)
        copy_quran.communicate(input=quran_text.encode("utf-8"))

def quran_rofi():
    surat = showSurat()
    if autoplay == "on":
        thr(target=surat.playMurotal).start()
        thr(target=surat.showAyat).start()
    else:
        surat.showAyat()

quran_rofi()
