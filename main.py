import os
import keyboard
import configparser
import time
import sys
import subprocess
import shutil

###########################
main_name = "Main Menu"
main_stars_count = 20
main_spacing = 0  # this will become the half of main_stars to center the text
FILE_dir_content = sys.path
key = ""  # This is used in MainMenu in the class get_key
list_files = []  # this is used to save the found files
locate_list = []
count = 0
dupe_prevention = ""
exe_name = ""
###########################
main_outline = "*" * main_stars_count
###########################
return_path = os.getcwd()


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def config_create():
    os.system("cls")  # Clear any unwanted text

    print("Creating config file...\n")
    time.sleep(1)  # wait's a second for the user to react

    for item in FILE_dir_content:  # Checks for python.exe file
        if item == r"C:\Program Files\Python39":
            os.chdir(item)
            break  # if path to Python39 exist, move on
    for item in os.listdir():
        if item.endswith("python.exe"):
            print("FOUND python.exe at: C:\Program Files\Python39")
            time.sleep(1.5)

            python_exe_path = os.path.join(os.getcwd() + "\python.exe")
            break
        else:
            python_exe_path = False
    if python_exe_path is False:
        python_exe_path = input("unable to find python.exe Please provide the path:")
    scan = input("What dir would you like to scan?\n:")
    os.chdir(return_path)  # After finding python.exe, Return

    with open("config.txt", "w") as config_file:
        config_file.write(f"[system]\npythonEXE = {python_exe_path}\n[paths]\nstartup = {return_path}\nscan_dir = {scan}")


def get_config(section, option):
    came_from = os.getcwd()
    os.chdir(return_path)  # First go back to the config.txt dir

    text_config = configparser.ConfigParser()
    text_config.read_file(open(r'config.txt'))

    data = text_config.get(section, option)
    os.chdir(came_from)
    return data


def menu(place):  # Creates the layout for the user to see
    global main_stars_count, main_name, main_spacing, main_outline, key

    class MainMenu:
        if place == "MainMenu":
            os.system("cls")  # Clear any text that might be in the CLI
            print(f"{main_outline}\n{main_name}\n{main_outline}")  # Print the top stars and text "Main Menu"
            print("1.Execute EXE File\n2.Create EXE File")

            while True:  # While loop to select option
                if keyboard.is_pressed("1"):
                    time.sleep(0.1)
                    execute_exe(get_config("paths", "scan_dir"))  # execute an exe file
                elif keyboard.is_pressed("2"):
                     create_exe()


def create_exe():
    scanned_output = []
    scanned_output_no_name = []
    scan_dir(get_config("paths", "scan_dir"), "files", None, None, scanned_output)
    scan_dir(get_config("paths", "scan_dir"), "files", None, None, scanned_output_no_name)
    filtered_output = []
    filtered_output_no_name = []
    locate_file(scanned_output, get_config("paths", "scan_dir"), ".py", None, None, filtered_output, False, True)
    locate_file(scanned_output_no_name, get_config("paths", "scan_dir"), ".py", None, None, filtered_output_no_name, False, False)


    count = 0
    for item in filtered_output:
        print(f"{count + 1}.{filtered_output[count]}")
        count = count + 1
    choise = input("Please Select a number: ")
    if choise.isdigit():
        choise = int(choise)
        if 1 <= choise <= len(filtered_output):
            choise = choise - 1
            print(filtered_output[choise])
            try:
                subprocess.run(["pyinstaller", "--onefile", filtered_output[choise]],check=True)
                print("done!")

                scanned_output = []
                scan_dir(get_config("paths", "scan_dir"), "files", None, None, scanned_output)
                count = 0

                is_done = []

                for item_2 in scanned_output:
                    count = count + 1

                    item_2_link = os.path.join(rf"{get_config('paths', 'scan_dir')},\{item_2}")
                    if item_2_link.endswith("dist"):


                        choise = int(choise)

                        path_shutil2 = filtered_output_no_name[choise]
                        path_shutil2 = str(path_shutil2)
                        item_2_str1 = str(item_2)

                        print(f"FOUND: {scanned_output[count]}")

                        print(f"this is path_shutil2: {path_shutil2}")
                        print(f"this is item2: {item_2_str1}")

                        shutil.move(item_2_str1, path_shutil2)
                        is_done.append("done1")


                    elif item_2_link.endswith("build"):

                        choise = int(choise)

                        path_shutil1 = filtered_output_no_name[choise]
                        path_shutil1 = str(path_shutil1)
                        item_2_str2 = str(item_2)


                        print(f"this is path_shutil1: {path_shutil1}")
                        print(f"this is item2: {item_2_str2}")

                        shutil.move(item_2_str2, path_shutil1)

                        print(f"FOUND: {scanned_output[count]}")

                        is_done.append("done2")

                if len(is_done) >= 2:

                    os.system("cls")
                    print("both files moved!")
                    time.sleep(1)
                    menu("MainMenu")

            except subprocess.CalledProcessError:
                print("ERROR")

        else: print("ERROR IN create_exe(): ERROR 1")
    else: print("ERROR IN create_exe(): ERROR 2")
def scan_dir(dir, add_1, add_2, Add_3, return_output):
    global list_files

    os.chdir(dir)
    output = []
    for item in os.listdir():
        item_path = os.path.join(dir, item)

        if add_1 is not None and item.endswith(add_1):
            return_output.append(item_path)
        elif add_2 is not None and item.endswith(add_2):
            return_output.append(item_path)
        elif Add_3 is not None and item.endswith(Add_3):
            return_output.append(item_path)
        elif (add_1 or add_2 or Add_3 == "files") and os.path.isdir(item_path):
            return_output.append(item_path)

    return return_output


def execute_exe(path):
    global list_files
    out_to_print = []
    filtered_list = []
    scan_dir(path, "files", None, None, out_to_print)
    config_dir = get_config("paths", "scan_dir")
    locate_file(out_to_print, config_dir, ".exe", None, None, filtered_list, False, True)
    count = 0
    for item in filtered_list:
        print(f"{count + 1}.{filtered_list[count]}")
        count = count + 1

    select = input("Select EXE File To Execute: ")
    if select.isdigit():
        select = int(select)
        if 1 <= select <= len(filtered_list):
            select = select - 1
            chose = filtered_list[select]
            print(f"you selected: {chose}")
            print(f"opening {chose}")
            time.sleep(1)
            os.startfile(chose)
            menu("MainMenu")

        else:
            print("ERROR IN EXECUTE_EXE(): ERROR 2")

    else:
        print("ERROR IN execute_exe(): ERROR 1")


def locate_file(list, dir, add_1, add_2, add_3, save_as, show_invalid, show_name):
    global dupe_prevention, exe_name
    loc = os.getcwd()
    list_name = []
    is_found = False

    for item in list:
        if not os.path.isdir(item):
            print("ERROR: LOCATE_FILES ONLY TAKES A LIST OF DIRECTORYS")
            quit()
    time.sleep(0.1)

    os.chdir(dir)
    debug_confirm1 = os.getcwd()
    print(f"entered {debug_confirm1}")

    for item in list:
        os.chdir(item)
        debug_confirm1 = os.getcwd()

        print(debug_confirm1)
        time.sleep(0.1)
        os.system("cls")

        readable_files = os.listdir()
        current_place = ""
        count = 1

        for item_in in readable_files:
            to_check = os.getcwd()
            current = to_check
            count = count + 1
            if add_1 is not None and item_in.endswith(add_1):
                exe_name = item_in
                is_found = True
                break
            elif add_2 is not None and item_in.endswith(add_2):
                exe_name = item_in
                is_found = True
                break
            elif add_3 is not None and item_in.endswith(add_3):
                exe_name = item_in
                is_found = True
                break
            else:
                is_found = False

        if is_found is False:

            if show_name is True:
                if show_invalid is True:
                    save_as.append(rf"{os.getcwd()}\NO FILE FOUND")
                    os.chdir(get_config("paths", "scan_dir"))
            elif show_name is False:
                 if show_invalid is True:
                     save_as.append(rf"{os.getcwd()}\ ")
                     os.chdir(get_config("paths", "scan_dir"))

        elif is_found is True:
            if show_name is True:
                save_as.append(rf"{os.getcwd()}\{exe_name}")
            elif show_name is False:
                save_as.append(rf"{os.getcwd()}")

        os.chdir(get_config("paths", "scan_dir"))

    return save_as


class PreCheck:
    if not os.path.exists("config.txt"):
        config_create()  # Start the setup
    else:
        print("Found Config.txt")


menu("MainMenu")