import PySimpleGUI as sg
import os.path

# First the window layout in 2 columns

file_list_column = [
    [
        sg.Text("Directory"),
        sg.In(size=(35, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(button_text="Select Diretory"),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(60, 20), key="-FILE LIST-"
        )
    ],
]

# For now will only show the name of the file that was chosen
image_viewer_column = [
    [sg.Text("Selet file aside")],
    [sg.Text(size=(60, 1), key="-TOUT-")],
]

# ----- Full layout -----
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]

window = sg.Window("Metadata Viewer", layout)

# Run the Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Folder name was filled in, make a list of files in the folder
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []
        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".png", ".pdf"))
        ]
        window["-FILE LIST-"].update(fnames)
    elif event == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            print(filename)
            window["-TOUT-"].update(filename)
        except:
            pass

window.close()