import PySimpleGUI as sg
import converter
import os

ROOT_FOLDER = os.path.abspath("my_file").split("/")[0]
FILE_NAME_LIST = []
FILE_DONE_LIST = []
PERCENT_COMPLETE = "0%"


def save_window():
  convert = False
  second_layout = [[
    sg.Text("Folder to save into"),
  ],
                   [
                     sg.In(size=(25, 1),
                           enable_events=True,
                           key="-FOLDER-",
                           default_text="/converted_audio__"),
                     sg.FolderBrowse(initial_folder="/home/oluwasegun"),
                   ],
                   [
                     sg.Button("Cancel", key="-CANCEL-"),
                     sg.Button("Convert", key="-CONVERT-")
                   ]]
  second_window = sg.Window("Save Options",
                            layout=second_layout,
                            keep_on_top=True)
  while True:
    event_, values_ = second_window.read()
    if event_ in (sg.WIN_CLOSED, "-CONVERT-", "-CANCEL-"):
      if event_ == "-CONVERT-":
        convert = True
      if values_["-FOLDER-"] == "/converted_audio__":
        folder_path = None
      else:
        folder_path = values_["-FOLDER-"]
      break
  second_window.close()
  return convert, folder_path


file_list_column = [
  [
    sg.Text("Folder/File"),
    sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
    sg.FolderBrowse(initial_folder="/home/oluwasegun", key="-BROWSE-"),
  ],
  [sg.Text("Queued files")],
  [
    sg.Listbox(values=[],
               enable_events=True,
               size=(40, 20),
               key="-FILE LIST-",
               select_mode=1)
  ],
  [
    sg.Button("Convert", key="-CONVERT-", disabled=True),
    sg.Button("Clear", key="-CLEAR LIST-", disabled=True),
  ],
]

file_preview_column = [[
  sg.Text(text="File name", visible=False, key="-FILE CONVERTED NAME-")
],
                       [
                         sg.ProgressBar(100,
                                        orientation='h',
                                        size=(20, 20),
                                        key="-PROGRESS BAR-",
                                        visible=False,
                                        bar_color=("Green", "White")),
                         sg.Text(text=PERCENT_COMPLETE, key="-PERCENT-")
                       ], [sg.Text("Converted files")],
                       [
                         sg.Listbox(values=[],
                                    enable_events=True,
                                    size=(40, 20),
                                    key="-FILE DONE LIST-")
                       ], [sg.Button("Finish", key="-FINISH-")]]

layout = [[
  sg.Column(file_list_column),
  # sg.VSeperator(),
  sg.Column(file_preview_column),
]]
sg.theme("DarkBlue13")
window = sg.Window(title="AV Converter", layout=layout, finalize=True)

while True:
  event, values = window.read()
  if event in ("OK", sg.WIN_CLOSED, "-FINISH-"):
    break
  if event == "-FOLDER-":
    if values["-BROWSE-"]:
      FILE_NAME_LIST = [
        file for file in converter.get_files(values["-BROWSE-"])
      ]
      window["-FILE LIST-"].update([file.name for file in FILE_NAME_LIST])
  elif event == "-FILE LIST-" and sg.popup_yes_no(
      "Do you want to remove this file from the queue?",
      keep_on_top=True) == "Yes":
    for file in FILE_NAME_LIST:
      if file.name == values["-FILE LIST-"][0]:
        FILE_NAME_LIST.remove(file)
    window["-FILE LIST-"].update([file.name for file in FILE_NAME_LIST])
  elif event == "-CLEAR LIST-" and sg.popup_yes_no(
      "Do you want to clear the whole queue?") == "Yes":
    FILE_NAME_LIST = []
    window["-FILE LIST-"].update(FILE_NAME_LIST)
  elif event == "-CONVERT-":
    proceed, directory = save_window()
    if proceed:
      window["-CONVERT-"].update(disabled=True)
      window["-CLEAR LIST-"].update(disabled=True)
      window["-BROWSE-"].update(disabled=True)

      count = 0
      for file in FILE_NAME_LIST:
        file_name = file.name
        # event, values = window.read()
        window["-PROGRESS BAR-"].update(visible=True)
        window["-FILE CONVERTED NAME-"].update(visible=True)
        file_path = file.path
        window["-FILE CONVERTED NAME-"].update(f"{file_name}")
        save_directory = converter.create_save_dir(dir_path=file_path,
                                                   save_folder=directory)
        print(file_path, save_directory, sep="\n")
        file_n = converter.convert_video_to_audio_moviepy(
          video_file=file_path, new_dir=save_directory)

        count += 1
        try:
          count / 1
        except ZeroDivisionError:
          percent = 0
        else:
          percent = round((count / len(FILE_NAME_LIST)) * 100, 1)
          PERCENT_COMPLETE = f"{percent}%"
          window["-PERCENT-"].update(PERCENT_COMPLETE)

        window["-PROGRESS BAR-"].update_bar(percent)
        FILE_DONE_LIST.append(file_n)
        window["-FILE DONE LIST-"].update(FILE_DONE_LIST)

  if FILE_NAME_LIST:
    window["-CONVERT-"].update(disabled=False)
    window["-CLEAR LIST-"].update(disabled=False)

window.close()
