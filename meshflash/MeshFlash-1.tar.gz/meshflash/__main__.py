# ----- <About> ----- #
#   Author: Zebus Zebus
#   Email: zebusjesus@pm.me
#   Date: 12-25-21
#   MeshFlash
#   Thank you to all the members of meshtastic that make this project possible
#
import PySimpleGUI as sg
import os
import requests
import subprocess
import time
from pubsub import pub
from zipfile import ZipFile

# ----- Menue Bar for all windows ----- #

menu_def = [['&File', ['&Properties', 'E&xit']]]

# ----- main window for application


# ----- Window 2 ----- #
def make_winMAIN():  ##define Frimware Window loayout and conents
    sg.theme('DarkAmber')
    sg.set_options(element_padding=(1, 1))
    layout = [
               [sg.Menu(menu_def, tearoff=False, pad=(200, 1))],
               [sg.Text('Hardware and  Firmware build selection')],
               [sg.Checkbox('T-Beam',key='-T-Beam-',enable_events=True),sg.Checkbox('heltec',key='-heltec-'),
                sg.Checkbox('T-LoRa',key='-T-LoRa-'),sg.Checkbox('LoRa Relay',key='-LoRa Relay-')],
               [sg.Checkbox('1.2.42',key='-1.2.42-'), sg.Checkbox('1.2.38',key='-1.2.38-'), sg.Checkbox('1.2.28',key='-1.2.28-'), sg.Checkbox('Hamster Nightly',key='-HN-')],
               [sg.Button('Download Firmware')],
               [sg.Text('Firmware'),sg.Input(key='_FILES_'), sg.FilesBrowse()],
               [sg.Text('spiff'),sg.Input(key='_FILES2_'), sg.FilesBrowse()],
               [sg.Text('system-info'),sg.Input(key='_FILES3_'), sg.FilesBrowse()],
               [sg.Text('You can then browse to the needed binary in the firmware folder.')],
               [sg.Text('Flashing Firmware requires you select a firmware, spiff and system-info file locations')],
               [sg.Button('Flash Firmware'), sg.Button('Update Firmware'), sg.Button('Erase Firmware')],
               [sg.Button('Backup Firmware'),sg.Input(key='_BACKUP_FILE_')],
               [sg.Button('Restore Frimware'),sg.Input(key='_RESTORE_FILE_'),sg.FilesBrowse()],
               [sg.Button('Close'), sg.Cancel()]
              ]
    return sg.Window('Firmware Utility', layout, finalize=True, no_titlebar=True, grab_anywhere=True)
# ------ /Window 2 ------ #

def main():
    WindowMain = make_winMAIN()
# --- Start Script Loop checking for events ----- #
    while True:             # Event Loop
        window, event, values = sg.read_all_windows()

# ----- Close Windows and program ----- #
        if window == sg.WIN_CLOSED:     # if all windows were closed
            break
        elif event == 'Exit':
            break
        if event == 'Close':
            window.close()
            if window == WindowMain:
                WindowMain = None


# ----- Download Firmware ----- #
        elif event == 'Download Firmware':
            firmwareID = 'NULL'
            firmwarRegion = 'NULL'
            binVersion = 'NULL'
            try:
                # ----- Firmware Downlaod URL----- #
                if values['-1.2.47-']:
                    binVersion = 'https://github.com/meshtastic/Meshtastic-device/releases/download/v1.2.47/firmware-1.2.47.zip'
                elif values['-1.2.48-']:
                    binVersion = 'https://github.com/meshtastic/Meshtastic-device/releases/download/v1.2.48.371335e/firmware-1.2.48.371335e.zip'
                elif values['-1.2.42-']:
                    binVersion = 'https://github.com/meshtastic/Meshtastic-device/releases/download/v1.2.42.2759c8d/firmware-1.2.42.2759c8d.zip'
                elif values['-HN-']:
                    dateBuild = (time.strftime("%y-%m-%d"))
                    hamURL = 'http://www.casler.org/meshtastic/nightly_builds/meshtastic_device_nightly_'
                    binVersion = hamURL+'20'+dateBuild+'.zip'
            except Exception:
                sg.popup('bin not pressent')
                # ----- /Firmware Download URL ----- #
            try:
                # ----- Donload Firmware File to zip ----- #
                url = binVersion
                firmwarefile = requests.get(url)
                open('firmware.zip', 'wb').write(firmwarefile.content)
                # ----- /Download Firmware File to zip ----- #

                # ---- Extract Frimware zip file ----- #
                with ZipFile('firmware.zip', 'r') as zipObj:
                    # Extract all the contents of zip file in current directory
                    zipObj.extractall(path='firmware')
            except Exception:
                sg.popup('error exctracting bin')
                os.system('echo exrror extracting bin >>error.log')
                #print('error extarcting bin')

        # ----- Flash Firmware ----- #
        elif event == 'Flash Firmware': # this command requires .sh files be able to be handled by the system, windows can us
            try:
                baudVALUE = '921600'
                os.system('python3 -m esptool --baud 921600 erase_flash')
                os.system('python3 -m esptool --baud 921600 write_flash 0x1000 '+values['_FILES3_'])
                os.system('python3 -m esptool --baud 921600 write_flash 0x00390000 '+values['_FILES2_'])
                os.system('python3 -m esptool --baud 921600 write_flash 0x10000 '+values['_FILES_'])
            except Exception:
                sg.popup('Flash Error')
                os.system('echo ERROR Flash Firmware Event >>error.log')
        # ----- /Flash Firmware ----- #

        # ----- Update firmware ----- #
        elif event == 'Update Firmware':# update firmware while keeping settings in place
            try:
                # User browses for the file the y need and the file chose is used as input for the flashing script
                # script must be present in the parent folder in order for flash function to work
                # os.system('sh device-update.sh -f '+values['_FILES_'])
                os.system('python3 -m esptool --baud 921600 write_flash 0x10000 '+values['_FILES_'] )
            except Exception:
                sg.popup('Firmware update error')
                os.system('echo ERROR Firmware update Event >>error.log')
        # ----- /Update firmware ----- #

        # ----- Erase Firmware ----- #
        elif event == 'Erase Firmware':
            try:
                os.system('python3 -m esptool --baud 921600 erase_flash')
            except Exception:
                sg.popup(' Erase Flash Error')
                os.system('echo ERROR Erasing Flash Firmware Event >>error.log')
        # ----- /Erase Firmware ----- #

        # ----- Backup Firmware ----- #
        elif event == 'Backup Firmware':
            try:
                os.system('python3 -m esptool --baud 921600 read_flash 0x00000 0x400000 '+values['_BACKUP_FILE_'])
            except Exception:
                sg.popup('Backup Error')
                os.system('echo ERROR Backup Firmware Event >>error.log')
        # ----- /Backup Firmware ----- #

        # ----- Restore Friimware ---- #

        elif event == 'Restore Firmware':
            try:
                os.system('python3 -m esptool --baud 921600 write_flash --flas_freq 80m 0x000000 '+values['_RESTORE_FILE_'])
            except Exception:
                output_window = window3RADIO
                sg.popup('Restore Flash Error')
                os.system('echo ERROR Restore Flash Firmware Event >>error.log')
        # ----- /Restore Firmware ----- #

# end Loops

if __name__ == '__main__':
    main()
