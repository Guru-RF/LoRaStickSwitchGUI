import PySimpleGUI as sg
import serial
import config

ser = serial.Serial()

def sendLoRa(data):
    global ser
    if not ser.isOpen():
        ser = serial.Serial(
            port=config.SerialPort, baudrate=4000000
        )

    data = "#sw#" + data + "\r\n"
    ser.write(bytes(data, 'ascii'))

    while ser.inWaiting() > 0:
        ser.read(1)
    
    return True    

sg.theme(config.Theme)   # Add a touch of color

layout = []

if config.PositionedVertical is False:
    layout = [[]]

    for i, val in enumerate(config.LoRaPorts):
        layout[0].append(sg.Button(val))
else:
    arr = [sg.Text("RF.Guru Remote RX")]
    layout.append(arr)

    for i, val in enumerate(config.LoRaPorts):
        arr = [sg.Button(val, size=(18, 1))]
        layout.append(arr)


# Create the Window
if config.PositionedVertical is True:
    windowTitle =  'RF.Guru'
else:
    windowTitle =  'RF.Guru Remote RX'
window = sg.Window(windowTitle, layout, keep_on_top=True, grab_anywhere=True)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    else:
        sendLoRa(config.LoRaPorts[event])

window.close()
