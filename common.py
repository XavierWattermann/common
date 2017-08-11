import requests
import os
from os import listdir
from os.path import isfile, join
import urllib
import csv
import time
from time import clock
import shutil
import sys
import random
import string
import json

sep = os.sep
cwd = os.getcwd()

def create_driver(use_chrome=True, chromedriver_path=r'C:\Users\xavi\AppData\Local\Continuum\Anaconda3\chromedriver.exe',
                  phantomjs_path=r"C:\Users\xavi\AppData\Local\Continuum\Anaconda3\phantomjs.exe"):
    """
    Creates a webdriver using Selenium
    :param use_chrome: True - use a chromedriver, False - Use PhantomJS
    :param chromedriver_path: Path to the chromedriver
    :param phantomjs_path: Path to PhantomJS
    :return: a driver
    """
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys

    if use_chrome:
        if is_file(chromedriver_path):
            return webdriver.Chrome(chromedriver_path)
        else:
            while True:
                print("Your chromedriver path doesn't appear to exist")
                path = input("Enter chromedriver path:")
                if isfile(path):
                    return webdriver.Chrome(path)
    else:
        if is_file(phantomjs_path):
            return webdriver.PhantomJS(phantomjs_path)
        else:
            while True:
                print("Your PhantomJS path doesn't appear to exist")
                path = input("Enter phantomJS path:")
                if isfile(path):
                    return webdriver.PhantomJS(path)

def copy(src, dst):
    shutil.copyfile(src, dst)


def flatten_list(lists):
    """
    Returns a flatten list from a list of lists.
        INPUT: [[1,2,3,4], [1,2,3], [3]]
        OUTPUT: [1, 2, 3, 4, 1, 2, 3, 3]
    :param lists: a 2D list
    :return: a flatten list with all those elements in one list.
    """
    flat_list = []
    for sublist in lists:
        for item in sublist:
            flat_list.append(item)
    return flat_list

def clock_start():
    """
    Starts the clock
    --Usage:
        import common
        start = common.clock_start()
        ----YOUR PROGRAM------
        common.clock_end(start)


    :return: the time the program starts
    """
    start = clock()
    print("Starting", start)
    return start

def clock_end(start):
    """
    Ends the clock
    --Usage:
        import common
        start = common.clock_start()
        ----YOUR PROGRAM------
        common.clock_end(start)
    :return: the time the program took - str
    """
    end = clock()
    print("Time Taken: {}".format(end - start))
    return "Time Taken: {}".format(end - start)

def info(*objs):
    """
    A method that prints out 1 or more object's properties so far including:
        - The object itself
        - Type of the object
        - Length of the object

    Sort of makes common.lengths() method obsolete.
    :param objs: a variable amount of objects. Where objects could be a list, tuple, str, etc
    :return: None - prints the results
    """
    for object in objs:
        if type(object) in [int, float]:
            print("Object is an int/float/long -- and therefore has no length")
            print('Length of your object converted to a string is:', len(str(object)))
        else:
            print('-' * 30)
            print("Object:", object, "\nType:", type(object), "\nLength:", len(object))
            print('-' * 30, '\n')

def soup_write(soup, file_path, file_ext=".txt"):
    """
    Writes a BeautifulSoup object to a textfile
    :param soup: the BeautifulSoup object
    :param file_path: The path for the textfile
    :param file_ext: The extension for the file; default is a .txt
    :return: None; creates a file with the soup object
    """
    from bs4 import BeautifulSoup
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
        Example:
            BeautifulSoup(<url>,<parser>).find_all("div", {"class": <"classname">})
            is simplifed with this method by using:
            results = common.find_all(soup_obj, "div", "class", "<classname>")

    :return: a list of items found by the search.
    """
    #  returns a soup object with find_all
    from bs4 import BeautifulSoup
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
    from bs4 import BeautifulSoup
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
    folder_path = os.path.join(user_home, 'Desktop', folder_name, '')
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
    return os.path.join(os.path.expanduser('~'), 'Desktop', '')

def create_folder(path_to_create, folder_name, alert_message=False):
    """
    Checks if a directory exists. If it does, simply return the path.
    If it doesn't, make the directory and then return the path.
    :param path_to_create: The 'root' directory of where the user wants the folder to be
    :param folder_name: the name of the folder to be created
    :return: a path to the newly created folder
    """

    new_path = os.path.join(path_to_create, folder_name, '')
    if not is_dir(new_path):
        print("Creating Folder at: " + new_path)
        os.makedirs(new_path)
    else:
        if alert_message:
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

        [hey, test, testword_1] would be returned. - type() == list
    :param file_path: the textfile to read in from
    :return: a list of items from the textfile
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

def write_json(data, file_path, write_mode='w', indent=2):
    """
    :param data: The data to write to a file
    :param file_path: Where the file should be written
    :param write_mode: w for write, a for append.
    :return: N/A
    """
    with open(file_path, write_mode) as f:
        json.dump(data, f, indent=indent)

def read_json(file_path):
    """
    Reads json from a file.
    :param file_path:
    :return:
    """
    if is_file(file_path):
        with open(file_path) as json_data:
            data = json.load(json_data)
            return data
    else:
        print("Your .JSON file doesn't appear to exist. Enter a new path")
        return read_json(input("New file path:"))

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

def files_in_directory(folder_path, return_full_path=True):
    #  returns a list of the files in a directory
    if is_dir(folder_path):
        files = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]
        if not return_full_path:
            return files
        else:
            full_files = []
            for item in files:
                full_files.append(folder_path + sep + item)
            return full_files
    else:
        print("Error - not a directory! - returning an empty list!")
        return []

def download(to_save, save_path):
    #  to_save: url to save
    #  save_path: directory + file name + file extension 
    try:
        if is_file(save_path):
            print('Item already exists!')
        else:
            urllib.request.urlretrieve(to_save, save_path)
            print(to_save + " was saved to: " + save_path)
    except:
        print("Error - Could not save!")
        print("File:", to_save, "\nPath:",save_path, end='\n\n')
        print("Unexpected error:", sys.exc_info()[0])

def replace_text(original_text, remove_characters="/\:*?\"<>|", replace_character=""):
    new_text = ""
    for c in remove_characters:
        new_text = original_text.replace(c, replace_character)
    return new_text

def print_text_file(text_file):
    #  prints out a textfile
    eazy_print(read_file(text_file))

def is_file(file_path):
    #  checks if a given path is actually a file
    return os.path.isfile(file_path)

def is_dir(folder_path):
    #  checks if a given folder path is actually a folder
    return os.path.isdir(folder_path)

def print_list(arg_list):
    """
    Method for looping through and printing a list.
    Good for testing.
    Can be called with eazy_print, ez_print, ez
    :param arg_list: The list to be printed
    :return: N/A
    """
    for item in arg_list:
        print(item)

def index_print(arg_list, index_offset=0):
    #  prints the index, along with the item
    #  index_offset: good for "human" stuff that starts at 1 and not 0
    for count, element in enumerate(arg_list, index_offset):
        print(count, element)

def zip_print(arg_list):
    #  prints a 2 item zipped list
    for a, b in arg_list:
        print(a, b)

def random_name(ext, file_length=6):
    """

    :param ext: the file extension, .mp4, .jpg, etc
    :param file_length: how long to make the filename
    :return: a random file name
    """
    file_name = ''
    letters = string.ascii_lowercase
    for i in range(file_length):
        file_name += random.choice(letters)

    file_name += str(random.randint(0,100)) + ext

    return file_name

#  Alternative Names -- since I forget what I call my other functions
eazy_print = print_list
ez_print = print_list
ez = print_list
view_text_file = print_text_file
get_driver = create_driver
create_soup = get_soup
