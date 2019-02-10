import csv
import json
import os
import random
import shutil
import string
import time
import urllib
from collections import OrderedDict, Counter
from multiprocessing.dummy import Pool

sep = os.sep
cwd = os.getcwd()


def create_driver(chromedriver_path, url=None, headless=False):
    """
    Creates a chrome webdriver using Selenium
    :param chromedriver_path: File path to the chromedriver executable
    :type chromedriver_path: str
    :param url: an optional argument to start the webdriver and go to a certain url
    :type url: str
    :param headless: an optional boolean argument to start the driver headless.
    :type headless: bool

    :return: a selenium webdriver with Chrome
    :rtype: selenium.webdriver.
    """
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
 
    chrome_options = Options()
    if is_file(chromedriver_path):
        if headless:
            chrome_options.add_argument("--headless")

        driver = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=chrome_options)

        if url:
            driver.get(url)
    else:
        print("Chromedriver Path doesn't exist!")
        return None

    return driver


def copy(src, dst):
    """
    Simple copy function because who the hell remembers to import shutil
    TODO: Better docs, and add a COPY_TO function that accepts a list of paths and
    will copy those items to another directory. -- add a 'move' flag for that
    """
    shutil.copyfile(src, dst)


def copy_to_desktop(file_path, folder_name=None):
    """
    Allows a user to copy a file, given it's file_path to the desktop.
        Things to add:
    - Better doc string
    - Allow file_path to be a LIST of file paths, so the user doesn't have to loop through themseleves
            But if they pass just a single file path, that will also work.
    - check if the file is a valid file
    - check if it's a directory
    - multithread copy?
    - better error checking
    - overwrite functionally, as a keyword argument.

    """

    if folder_name is None:
        folder_name = get_desktop()
    else:
        folder_name = create_desktop_folder(folder_name, alert_message=False)

    save_directory = os.path.join(folder_name, os.path.basename(file_path))

    if not is_file(file_path):
        print("{} is not a file!".format(file_path))
        return

    try:
        copy(file_path, save_directory)
        print("File: {}, was copied to: {}".format(file_path, save_directory))
    except shutil.SameFileError:
        print("File is already there!")


def is_dir(folder_path):
    """
    Simple 'wrapper' for os.path.isdir(), because importing os and typing that is too much work...
    :param folder_path: The path to check for existence.
    :type folder_path: str
    :return: True (folder exists), False (folder doesn't exist)
    :rtype: bool
    """
    return os.path.isdir(folder_path)


def flatten_list(lists, return_unique=False):
    """
    Returns a flatten list from a list of lists.
        INPUT: [[1,2,3,4], [1,2,3], [3]]
        OUTPUT: [1, 2, 3, 4, 1, 2, 3, 3]
    :param lists: a 2D list
    :type lists: list
    :param return_unique: can return only the unique items from the newly flatten list
    :type return_unique: bool
    :return: a flatten list with all those elements in one list.
    """
    flat_list = []
    for sublist in lists:
        for item in sublist:
            flat_list.append(item)

    if return_unique:
        return unique_items(flat_list) 

    return flat_list


def frequency(iterable, common_count=None):
    """
    Simple "wrapper" for collections.Counter which returns a frequency on various iterable data types (lists, tuples)

    Example:
    "aaaabccc" => {'a': 4, 'b': 1, 'c': 3}

    count is an optional param which returns N amount of items - int
    :param iterable: a list, tuple, set, etc of items
    :type iterable: list
    :param common_count: to return a subset of the items with only the N most popular items.
    :type common_count: int
    :return A counter (a dictionary with keys, and the value is the number of times the keys are present)
    :rtype: collections.Counter
    """
    if common_count and isinstance(common_count, int):
        return Counter(iterable).most_common(common_count)

    return Counter(iterable)


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
    start = time.clock()
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
    end = time.clock()
    print("Time Taken: {}".format(end - start))
    return "Time Taken: {}".format(end - start)


def info(*objs, limit_output=True):
    """
    A method that prints out 1 or more object's properties so far including:
        - The object itself
        - Type of the object
        - Length of the object
    Sort of makes common.lengths() method obsolete.

    :param objs: a variable amount of objects. Where objects could be a list, tuple, str, etc
    :type objs: unknown(list, tuple, dict, set)

    :param limit_output: limits the output of very large objects. 
    :type limit_output: bool

    :return: None - prints the results
    """
    for obj in objs:
        if isinstance(obj, (int, float, complex)):
            print("Object is an int/float/complex -- and therefore has no length")
            print('Length of your object converted to a string is:', len(str(obj)))
        else:
            print('-' * 200)
            
            if limit_output:
                print("50 first entries of Object: {}\nType: {}\nLength: {}".format(obj[0:50], type(obj), len(obj)))
            else:
                print("Object: {}\nType: {}\nLength: {}".format(obj, type(obj), len(obj)))
            
            print("Frequency: {}".format(frequency(obj, common_count=10)))
            
            if isinstance(obj, list): 
                print("Unique Items: {}".format(unique_items(obj)))
            
            print("Available Public Attributes: {}".format([attr for attr in dir(obj) if '__' not in attr]))

            print('-' * 200, '\n')


def soup_write(soup, file_path, file_ext=".txt"):
    """
    Writes a BeautifulSoup object to a textfile
    :param soup: the BeautifulSoup object
    :type soup: bs4.BeautifulSoup
    :param file_path: The path for the textfile
    :type file_path: str
    :param file_ext: The extension for the file; default is a .txt
    :type file_ext: str
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
    :type soup: bs4.BeautifulSoup
    :param first: The first item to search for. Example: div
    :type first: str
    :param second: the second aspect to search for. The key in the key:value pair. Example: class
    :type second: str
    :param third: The third aspect, which is the value in the key: value pair. Example: <class-name>
        Example:
            BeautifulSoup(<url>,<parser>).find_all("div", {"class": <"classname">})
            is simplifed with this method by using:
            results = common.find_all(soup_obj, "div", "class", "<classname>")
    :type third: str
    :return: a list of items found by the search.
    """
    #  returns a soup object with find_all
    try:
        items = soup.find_all(first, {second: third})
    except Exception as error:
        print("There was an error trying to find all", error)
        return None
    if not items:
        print("Didn't find anything!")
    return items


def get_soup(url, parser="html.parser"):
    """
    A quicker way to create a BeautifulSoup object, just provide the url that needs to be parsed & a BS obj is returned
    :param url: The url of the site that needs to be parsed.
    :type url: str
    :param parser: the parser to use, by default html.parser (built into BS) is used. Other options are xml, lxml.
    :TODO: Do a better check to see if the passed 'url' is a selenium webdriver
    :type parser: str
    :return: a BeautifulSoup object.
    """
    from bs4 import BeautifulSoup
    import requests
    try:
        if 'webdriver' in str(type(url)):  # a pretty weak check to see if 'url' is really a selenium webdriver
            # we can use a webdriver's page_source to get the content of the current site.
            soup = BeautifulSoup(url.page_source, parser)
        elif is_file(url):  # the url is a file, try to open it and parse.
            soup = BeautifulSoup(open(url, 'r'), parser)
        else:
            page = requests.get(url).content
            soup = BeautifulSoup(page, parser)
    except Exception as e:
        print("An error has occurred with common.get_soup(). Here is the error message: {}".format(e))
        return None

    return soup


def check_valid_site(url, print_status=False):
    """
    Checks if a passed URL is valid. If the status code from the site isn't 200, than it isn't valid.
    :param url: a url to check
    :type url: str
    :param print_status: Print if the passed site is valid or not
    :type print_status: bool
    :return: True(site is valid) or False(site isn't valid; 404)
    :rtype: bool
    """
    import requests
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
    except Exception as e:
        print("It broke on", url)
        print("Error: ", e)


def lengths(*args):
    """
    Returns the length of multiple objects. Good for testing.
    :param args: multiple argument for N amount of objects (usually lists)
    :type args: iterable
    :return: None
    """
    for i, obj in enumerate(args):
        print("Item", i, obj, "has a length of:", len(obj))


def create_desktop_folder(folder_name, alert_message=True):
    """
    Creates a folder on the user's desktop
    :param folder_name: the name of the folder on the desktop
    :type folder_name: str
    :param alert_message: verbose mode; add a print statement that the folder was created and the path
    :type alert_message: bool
    :return: the path to the new folder.
    :rtype: str
    """
    #  given a folder name, a folder with that name is created on the Desktop
    return create_folder(get_desktop(), folder_name, alert_message=alert_message)


def get_desktop():
    """
    gets a path to the user's desktop
    :return: A path to the user's desktop
    :rtype: str
    """
    return os.path.join(os.path.expanduser('~'), 'Desktop', '')


def create_folder(path_to_create, folder_name=None, alert_message=False):
    """
    Checks if a directory exists. If it does, simply return the path.
    If it doesn't, make the directory and then return the path.
    :param path_to_create: The 'root' directory of where the user wants the folder to be
    :type path_to_create: str
    :param folder_name: the name of the folder to be created
    :type folder_name: str
    :param alert_message: (bool) - Prints 'Path already exists' if True.
    :type alert_message: bool
    :return: a path to the newly created folder
    :rtype: str
    """
    if folder_name:
        new_path = os.path.join(path_to_create, folder_name, '')
    else:
        new_path = path_to_create
    if not is_dir(new_path):
        print("Creating Folder at: " + new_path)
        os.makedirs(new_path)
    else:
        if alert_message:
            print("Path already exists!")

    return new_path


def read_file(file_path, sort=False, return_string=False, join_character=" "):
    """
    Reads in a textfile and returns a list of that file.
    Works best (or possibly only) if the textfile is formatted with a word/sentence on each line.
        Example:
            hey
            test
            testword_1
        [hey, test, testword_1] would be returned. - type() == list
    :param file_path: the textfile to read in from
    :type file_path: str
    :param sort: boolean to sort the read in list.
    :type sort: bool
    :param return_string: can return the textfile as one giant string.
    :type return_string: bool
    :param join_character: the character to use/seperate when return_string=True, by default it's
    an empty space. Other common characters could be "-", ".", "\n"
    :type join_character: str

    :return: a list of items from the textfile
    :rtype list (unless return_string; then str)
    """
    #  reads from a textfile into a list, and returns that list
    if is_file(file_path):
        with open(file_path) as f:
            file_list = f.read().splitlines()
    else:
        print("Your file doesn't appear to exist.")
        path = input("Enter new file path -- 'c' to cancel")
        if path == 'c':
            print("Path not found -- returning an empty list")
            return []
        return read_file(input("New file path: "))

    if return_string:
        return join_character.join(file_list)

    if sort and isinstance(file_list, list):
        file_list.sort()

    return file_list


def read_csv(file_path):
    #  reads from a (csv)textfile into a list, and returns that list
    if is_file(file_path):
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            file_list = list(reader)
    else:
        print("Your file doesn't appear to exist. Enter a new path")
        return read_file(input("New file path: "))

    return file_list


def write_json(data, file_path, write_mode='w', indent=2, print_message=False):
    """
    :param data: The data to write to a file
    :param file_path: Where the file should be written
    :param write_mode: w for write, a for append.
    :param indent: (int) - indent to provide for the json, 2 usually looks pretty good.
    :param print_message: boolean if a print message should be made if the file was written (default: false)
    :return: None
    """
    with open(file_path, write_mode) as f:
        json.dump(data, f, indent=indent)
        if print_message:
            print("JSON file was written to: {}".format(file_path))


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
        print("Your .JSON file doesn't appear to exist.")
        path = input("Enter new file path -- 'c' to cancel")
        if path == 'c':
            print("Path not found -- returning 'None'")
            return None
        return read_json(input("New file path:"))


def write_to_file(write_list, file_path, write_mode='a'):
    #  writes a list to a textfile
    if isinstance(write_list, list):
        with open(file_path, write_mode) as my_file:
            for item in write_list:
                my_file.write(str(item) + "\n")
    else:
        #  if you didn't pass a list, this will hopefully write whatever you passed anyways; ya goofed
        writer = open(file_path, write_mode, encoding="utf-8")
        writer.write(write_list)


def files_in_directory(folder_path=None, recursive=False, return_full_path=True, file_type=None):
    """
    Returns the files in a given directory.
    By default, only returns the files in the immediate directory(folder_path).
        Setting recursive to True, will get all files.
    :param folder_path: the path to look for files
    :type folder_path: str
    :param recursive: to search in the folder_path for any subfolders to get more files
    :type recursive: bool
    :param return_full_path: return the absolute path for each file. Usually desired, especially for recursive mode.
    :type return_full_path: bool
    :param file_type: a list or string representing file types to return. passing '.txt' will return only .txt files.
    :type file_type: str or list/tuple/set of strings
    :return: a list of file paths
    :rtype: list
    """
    file_list = []
    if not folder_path:  # if nothing is passed, use the current directory
        folder_path = '.'

    if not is_dir(folder_path):
        print("{} is not a folder! - Returning an empty list".format(folder_path))
        return []

    for current_folder, subdirectories, files in os.walk(folder_path):
        for file_path in files:
            if return_full_path:
                file_list.append(os.path.join(current_folder, file_path))
            else:
                file_list.append(file_path)
        if not recursive:  # this means we only want the current directory's file; nothing more
            break

    if file_type:
        if isinstance(file_type, (list, tuple)):
            # unlikely, but removes not strings from file_types
            file_type = list(filter(lambda f_type: isinstance(f_type, str), file_type))

            file_list = list(filter(lambda f: f.endswith(tuple(file_type)), file_list))
        elif isinstance(file_type, str):
            file_list = list(filter(lambda f: f.endswith(file_type), file_list))
        else:
            print("Invalid type for parameter 'file_type' -- Must be a list, tuple or str")

    return file_list


def folders_in_directory(folder_path, recursive=False, return_full_path=True):
    """
    Similar to files_in_directory(), this function returns the folder paths in a given directory.
    By default, only returns the immediate subdirectories in the folder_path.
        Setting recursive to True, will get all subfolders.
    :param folder_path: (str) - The root folder to start
    :type folder_path: str
    :param recursive: (bool) - to get all the folders in the sub directories, and the sub-sub directories, and so on.
    :type recursive: bool
    :param return_full_path: (bool) - to return the full/absolute path of the folder, not just the name.
    :type return_full_path: bool
    :return: a list of folder paths
    :rtype: bool
    """
    folder_list = []
    if not is_dir(folder_path):
        print("{} is not a folder! Returning an empty list".format(folder_path))
        return []
    if folder_path == '.':
        folder_path = os.getcwd()
    for current_folder, subdirectories, files in os.walk(folder_path):
        for sub_path in subdirectories:
            if return_full_path:
                folder_list.append(os.path.join(current_folder, sub_path))
            else:
                folder_list.append(sub_path)
        if not recursive:  # this means we only want the current directory's subdirectories; nothing more
            break
    return folder_list


def download(to_save, save_path, verbose=False):
    """
    Downloads a file from the internet using urllib.request.urlretrieve

    File needs to be a direct link to an image, .mp3, .mp4, etc
    The save_path needs to be the FULL path of where to save the file.

    So if you wanted to save <URL> to a folder on your desktop you would do:
        common.download(URL, 'home/USER/Desktop/FOLDER/file_name.EXTENSION')

    :param to_save: the URL of the file to save
    :type to_save: str
    :param save_path: Where to save the file
    :type save_path: str
    :param verbose: to print out additional information about the status of the download
    :type verbose: bool
    :return: None
    """
    try:
        if is_file(save_path):  # if it already exists, we do nothing. TODO: Maybe add overwrite option?
            if verbose:
                print('Item already exists!')
        else:
            urllib.request.urlretrieve(to_save, save_path)

            #  if verbose: TODO: what to do here
            print(to_save + " was saved to: " + save_path)
    except Exception as e:
        print("Error - Could not save!")
        print("File:", to_save, "\nPath:", save_path, '\n')
        print(e)


def ez_download(list_of_items, save_directory=None, multithreaded=False):
    """
    Eazy way to download a list of items.
    For a multithreaded approach, multithread_download can be called
    :param list_of_items: a list to loop through and download
    :param save_directory: where to save the items, if None is provided, saves on the desktop
    :param multithreaded: if True, calls multithread_download
    :return: N/A
    """
    if not save_directory:  # no save directory given means we save it to the desktop
        save_directory = create_desktop_folder('python_download')

    #  TODO: add a verbose mode for this as well?
    # Basically, need a way to let the user know shit is being downloaded without being annoying
    print("Starting Download...")
    if multithreaded:
        multithread_download(list_of_urls=list_of_items, save_directory=save_directory)
    else:
        for item in list_of_items:
            save_path = os.path.join(save_directory, os.path.split(item)[1])
            download(to_save=item, save_path=save_path)
    print("\tEnding Download...")


def multithread_download(list_of_urls, threads=6, save_directory=None):
    """
    Uses Python's multiprocessing module to call common.download with multiple threads
    Requires that the passed list of items contains direct links to media

    How it works:
    The pool object has a .map() function, which typically takes two parameters
        - a function
        - a list
    Map then takes each item from the list, and applies it to the function.

    In this case, we're taking each file from the list, and calling common.download() to download the file.

    Common.download() also takes two parameters:
        - the file to download
        - the save directory

    So I use a lambda function to take the file from the list, and call common.download() with that file,
    and the passed save_directory and splitting the file with os.path.split(FILE)[1] to get the tail of the file,
    which is hopefully NAME_OF_FILE.<EXTENSION>


    :param list_of_urls: a list of urls(that are direct links to media(.jpg, .mp3, etc)) that can be saved with
    urllib.request.urlretrieve aka common.download()
    :type list_of_urls: list
    :param threads: the number of threads to use; by default 6 is used
    :type threads: int
    :param save_directory: where to save the items
    :type save_directory: str
    :return: None
    """
    if not save_directory:
        save_directory = create_desktop_folder('multithread_download')
    
    pool = Pool(threads)
    pool.map(lambda file_url: download(file_url, os.path.join(save_directory, os.path.split(file_url)[1])),
             list_of_urls)


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


def index_print(arg_list, starting_index=0):
    #  prints the index, along with the item
    #  index_offset: good for "human" stuff that starts at 1 and not 0
    for count, element in enumerate(arg_list, starting_index):
        print(count, element)


def zip_print(arg_list):
    #  prints a 2 item zipped list
    for a, b in arg_list:
        print(a, b)


def random_name(ext, file_length=6):
    """
    :param ext: the file extension, .mp4, .jpg, etc
    :type ext: str
    :param file_length: how long to make the filename
    :type file_length: int
    :return: a random file name
    :rtype: str
    """
    file_name = ''
    letters = string.ascii_lowercase
    for i in range(file_length):
        file_name += random.choice(letters)

    file_name += str(random.randint(0, 100)) + ext

    return file_name


def continuous_input(message=None, end_word='stop'):
    """
    Gets multiple input from the user until they enter the 'end_word'

    Returns a list of user inputted values
    """
    if not message:
        message = "Please enter items and enter '{}' to quit:".format(end_word)

    items = []
    while True:
        temp_item = input(message)
        if temp_item == end_word:
            break
        else:
            items.append(temp_item)
    return items


def list_choice(list_of_items):
    """
    Loops through a list of items and allows the user to select the index to return that item in the list
    Good for quickly making menus
    """
    print("|INDEX|\t|CHOICE|")
    index_print(list_of_items, starting_index=1)
    choice = input("Enter the index of the item to return\n>>>")
    try:
        item_to_return = list_of_items[int(choice) - 1]  # handle starting at 1
        return item_to_return
    except IndexError:
        print("The index you provided is not in the list")
        print("Your list has an a length of {}".format(len(list_of_items)))
    except ValueError:
        print("You didn't enter an integer!")

    return list_choice(list_of_items)  # if this reaches, it means we got invalid input


def sleep(time_to_sleep, use_minutes=False, message=None, end_message=None):
    if type(time_to_sleep) not in [int, float]:
        print("time_to_sleep variable needs to be an int or a float!")
        return
    if use_minutes:
        time_to_sleep *= 60
    if message is None:
        message = "Sleeping for {} seconds".format(time_to_sleep)
    if end_message is None:
        end_message = "Finished Sleeping"

    if message:  # if message is set to False, we don't print anything.
        print(message)

    time.sleep(time_to_sleep)

    if end_message: 
        print(end_message)


def time_print(user_list, time_to_sleep=1, use_minutes=False, sleep_message=False):
    """
    Prints a user's list with sleeping for N number of seconds between each item in the list

    I think I've only needed to do something like this once for testing...
    I can't really think of a use-case for this right now...
    """
    if not isinstance(time_to_sleep, (int, float)):
        print("time_to_sleep variable needs to be an int or a float!")
        return
    if use_minutes:
        time_to_sleep *= 60

    for item in user_list:
        print(item)
        if sleep_message:
            print("\tSleeping for {} seconds".format(time_to_sleep))


def unique_items(user_list, preserve_order=False):
    """
    removes duplicates elements from a list, by simply making it a set and then a list again
    :param user_list: the user's list that the unique items will be returned
    :preserve_order: boolean - if the order matters for your list this should be set to True
    :type user_list: list
    :param preserve_order: attempts to keep the order of the items
    :type preserve_order: bool
    :return: a list with only unique items; no duplicates
    :rtype: list
    """
    if not isinstance(user_list, list): 
        print("you must pass a list! Returning None")
        return None

    if preserve_order:
        return list(OrderedDict.fromkeys(user_list))  # may not need to do this in later versions of Python3
    else:
        return list(set(user_list))


def list_difference(list1, list2):
    """
    Probably the most useful "list/set" operation for my use
    Takes list1 and returns the items from list1 that AREN'T in list2.
    so 
    a = {1,2,3}
    b = {2,3,4}
    a - b == {1}

    Useful if you have, for example, a bunch of urls to save. list1 could be the urls to save,
    and list2 could be a list of urls that are already saved. Using the function would return a 
    list of only new urls that need to be saved
    :param list1 - the first list...
    :type list1: list
    :param list2 - the second list...
    :type list2: list
    :return: a list with only items that are in list1 and NOT in list2
    :rtype: list
    """

    return list(set(list1) - set(list2))


def file_info(file_path):
    """
    Gives metadata about a file, including:
        -
    :param file_path: the path of the file on the system
    :type file_path: str
    :return: a dict containing the file meta data
    :rtype: dict
    """
    data = {}
    if not isfile(file_path):
        print("File path({}) doesn't exist!".format(file_path))
        return {}

    data['directory'] = os.path.dirname(file_path)
    data['name'] = os.path.basename(file_path)
    data['extension'] = os.path.splitext(file_path)[-1]

    return data


def directory_to_dict(directory=None):
    """
    WIP: Takes a directory and produces a .json file on the directory's contents
    This will include subdirectories, files, and stats about them (how many folders, files, etc)

    Extra flags can give more meta data information -- like file size? date modified/created?
    TODO: Add Param Comments
    """
    data = {}
    all_paths = []
    all_subdirectories = []  # this might just be a subset of all_paths
    all_files = []
    # TODO: validate directory; if it's none, use c.w.d, else check if it's a valid path

    for path, subdirectories, files in os.walk(directory):
        pass


def randint(a, b):
    """
    Simple wrapper for random.randint(), which I get tired of having to import to generate a rand between two numbers.
        randint doc: Return a random integer N such that a <= N <= b. Alias for randrange(a, b+1).
    :param a:
    :type a: int
    :param b:
    :type b: int
    :return: a random integer between a and b
    :rtype: int
    """
    if all([isinstance(a, int), isinstance(b, int)]):
        return random.randint(a, b)
    else:
        raise ValueError("You must pass integers!")


#  Alternative Names -- since I forget what I call my other functions
eazy_print = print_list
easy_print = print_list
ez_print = print_list
ez = print_list
view_text_file = print_text_file
get_driver = create_driver
isdir = is_dir
isfile = is_file
create_soup = get_soup
get_files_in_directory = files_in_directory
get_files = files_in_directory
get_folders = folders_in_directory
get_folders_in_directory = folders_in_directory
easy_download = ez_download
remove_duplicates = unique_items
write_file = write_to_file
directory_to_json = directory_to_dict
