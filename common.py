try:
    import requests
    from bs4 import BeautifulSoup
    import os
    from os import listdir
    from os.path import isfile, join
    import urllib
    import csv
    import urlparse2
    from selenium import webdriver
    import simplejson
except Exception as error:
    pass
    #print("Couldn't get module. Error: ", error)



def help():
    print("Here are the current functions for common.py:")
    print('''get_soup(url, parser="html.parser - given a url, a request object is created using the given url.


soup_write(soup, file_path, file_ext=".txt") - writes a BeautifulSoup Object to a textfile to be saved later

soup_find_all(soup, first, second, third) - returns a find all request on a soup object

check_valid_site(url) - given a url, checks if the URL is a valid site

create_desktop_folder(folder_name) - creates a folder on the desktop *returns path to the new folder

create_folder(path_to_create, folder_name) - creates a folder with a passed path and name *returns new path

read_file(file_path) - reads a textfile with a passed path *returns list of the textfile

def read_csv(file_path) - reads a CSV textfile *returns a list

read_json(file_path) - Currently doesn't work - but returns a JSON object

write_to_file(write_list, file_path, write_mode='a') - writes a list to a textfile 

write_json(data, file_path, write_mode='w') - 

files_in_directory(folder_path, return_full_path=False) - 

download(to_save, save_path) - 

replace_text(original_text, remove_characters="/\:*?\"<>|", replace_character="") - 

print_text_file(text_file) - prints a textfile with a passed path

is_file(file_path) - checks if a passed path is an actual file *returns Boolean

is_dir(folder_path) - checks if a passed path is an actual directory *returns Boolean

print_list(arg_list) - prints a list - can also use ez_print(list) or eazy_print(list)

zip_print(arg_list) - prints a zipped list with two variables. so like for a, b in arg_list


''')


def soup_write(soup, file_path, file_ext=".txt"):
    """
    Writes a BeautifulSoup object to a textfile
    :param soup: the BeautifulSoup object
    :param file_path: The path for the textfile
    :param file_ext: The extension for the file; default is a .txt
    :return: None; creates a file with the soup object
    """
    html = soup.prettify("utf-8")
    with open(file_path + file_ext, "wb") as file:
        file.write(html)

    print("FILE PATH + file_ext =", file_path+file_ext)


def find_all(soup, first, second, third):
    """
    A simpler (sorta...) method to BeautifulSoup.find_all
    :param soup: A BeautifulSoup object
    :param first: The first item to search for. Example: div
    :param second: the second aspect to search for. The key in the key:value pair. Example: class
    :param third: The third aspect, which is the value in the key: value pair. Example: <class-name>
    :return: a list of items found by the search.
    """
    #  returns a soup object with find_all
    try:
        items = soup.find_all(first, {second:third})
    except Exception as error:
        print("There was an error trying to find all", error)
        return None
    if items == None or items == []:
        print("Didn't find anything!")
    return items


def get_soup(url, parser="html.parser"):
    """
    A quicker way to create a BeautifulSoup object, just provide the url that needs to be parsed & a BS obj is returned
    :param url: The url of the site that needs to be parsed.
    :param parser: the parser to use, by default html.parser (built into BS) is used. Other options are xml, lxml.
    :TODO: if url (needs to be renamed) is a file, open the file and create a bs obj on that file.
    :return: a BeautifulSoup object.
    """
    #  given a url, a request object is created using the given url
    #  then a soup object is created using the page object, and the soup object is returned
    page = requests.get(url).content
    try:
        soup = BeautifulSoup(page, parser)
    except(Exception):
        print("Error with parser?")
        soup = BeautifulSoup(page)
    return soup


def check_valid_site(url, print_status=False):
    """
    Checks if a passed URL is valid. If the status code from the site isn't 200, than it isn't valid.
    :param url: a url to check
    :param print_status: Print if the passed site is valid or not
    :return: True(site is valid) or False(site isn't valid; 404)
    """
    try:
        request = requests.get(url)
        status_code = request.status_code
        if status_code == 200:  # return request.status_code == 200 could be used,
            if print_status:
                print(url, "was a valid site")
            return True
        else:
            if print_status:
                print(url, "was not a valid status, here's the status code:", status_code)
            return False
    except:
        print("It broke on", url)

def lengths(*args):
    """
    Returns the length of multiple objects. Good for testing.
    :param args: multiple argument for N amount of objects (usually lists)
    :return:
    """
    for item in enumerate(args):
        i, obj = item
        print("Item", i, obj, "has a length of:", len(obj))


def create_desktop_folder(folder_name):
    """
    Creates a folder on the user's desktop
    :param folder_name: the name of the folder on the desktop
    :return: the path to the new folder.
    """
    #  given a folder name, a folder with that name is created on the Desktop
    user_home = os.path.expanduser('~')
    sep = os.sep
    folder_path = user_home + sep + 'Desktop' + sep + folder_name + sep
    if not is_dir(folder_path):
        print("Creating Folder at: " + folder_path)
        os.makedirs(folder_path)
    else:
        print("The folder appears to already exist!")
    return folder_path

def get_desktop():
    """
    gets a path to the user's desktop
    :return: A path to the user's desktop
    """
    return os.path.expanduser('~') + os.sep + 'Desktop' + os.sep


def create_folder(path_to_create, folder_name):
    """
    Creates a folder where ever the user wants
    :param path_to_create: The 'root' directory of where the user wants the folder to be
    :param folder_name: the name of the folder to be created
    :return: a path to the newly created folder
    """
    sep = os.sep
    #  create a new folder given a directory, and call the folder by the passed folder_name
    new_path = path_to_create + sep  + folder_name + sep
    if not is_dir(new_path):
        print("Creating Folder at: " + new_path)
        os.makedirs(new_path)
    else:
        print("Path already exists!")

    return new_path


def read_file(file_path):
    """
    Reads in a textfile and returns a list of that file.
    Works best (or possibly only) if the textfile is formatted with a word/sentence on each line.
        Example:
            hey
            test
            testword_1

        a list containting hey, test, testword_1 would be returned.
    :param file_path:
    :return:
    """
    #  reads from a textfile into a list, and returns that list
    if is_file(file_path):
        file_list = []
        with open(file_path) as f:
            file_list = f.read().splitlines()
    else:
        print("Your file doesn't appear to exist. Enter a new path")
        return read_file(input("New file path: "))

    return file_list


def read_csv(file_path):
    #  reads from a (csv)textfile into a list, and returns that list
    if is_file(file_path):
        file_list = []
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            file_list = list(reader)
    else:
        print("Your file doesn't appear to exist. Enter a new path")
        return read_file(input("New file path: "))

    return file_list


def read_json(file_path):
    """
    Needs to be modified to support the builtin json library.
    :param file_path:
    :return:
    """
    with open(file_path, 'r') as f:
        try:
            data = simplejson.load(f)
        except ValueError:
            print("Value Error")
            data = {}
    return data


def write_to_file(write_list, file_path, write_mode='a'):
    #  writes a list to a textfile
    if type(write_list) == list:
        with open(file_path, write_mode) as my_file:
            for item in write_list:
                my_file.write(str(item) + "\n")
    else:
        #  if you didn't pass a list, this will hopefully write whatever you passed anyways; ya goofed
        writer = open(file_path, write_mode, encoding="utf-8")
        writer.write(write_list)

def write_json(data, file_path, write_mode='w'):
    with open(file_path, write_mode) as f:
        simplejson.dump(data, f)


def files_in_directory(folder_path, return_full_path=False):
    #  returns a list of the files in a directory
    if is_dir(folder_path):
        files = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]
        if not return_full_path:
            return files
        else:
            full_files = []
            for item in files:
                full_files.append(folder_path + "\\" + item)
            return full_files
    else:
        print("Error - not a directory! - returning an empty list!")
        return []


def download(to_save, save_path):
    #  to_save: url to save
    #  save_path: directory + file name + file extension 
    try:
        urllib.urlretrieve(to_save, save_path)
        print(to_save + " was saved to: " + save_path)
    except:
        print("Error - Could not save!")


def replace_text(original_text, remove_characters="/\:*?\"<>|", replace_character=""):
    new_text = ""
    for c in remove_characters:
        new_text = original_text.replace(c, replace_character)
    return new_text
        

def print_text_file(text_file):
    #  prints out a textfile
    eazy_print(read_file(text_file))


def view_text_file(text_file):
    #  alternate named, that prints out a text file
    print_text_file(text_file)


def is_file(file_path):
    #  checks if a given path is actually a file
    return os.path.isfile(file_path)


def is_dir(folder_path):
    #  checks if a given folder path is actually a folder
    return os.path.isdir(folder_path)


def print_list(arg_list):
    #  eazy print - good for testing.
    for item in arg_list:
        print(item)


def index_print(arg_list, index_offset=0):
    #  prints the index, along with the item
    #  index_offset: good for "human" stuff that starts at 1 and not 0
    for count, element in enumerate(arg_list, index_offset):
        print(count, element)


def ez_print(arg_list):
    #  alternate print list
    print_list(arg_list)


def ez(arg_list):
    #  alternate print list
    print_list(arg_list)


def eazy_print(arg_list):
    #  alternate print list
    print_list(arg_list)


def zip_print(arg_list):
    #  prints a 2 item zipped list
    for a, b in arg_list:
        print(a, b)


