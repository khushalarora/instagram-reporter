# coding=utf-8
#!/usr/bin/env python3

from libs.check_modules import check_modules
from sys import exit
from os import _exit

check_modules()

from os import path

from libs.logo import print_logo
from libs.utils import print_success
from libs.utils import print_error
from libs.utils import ask_question
from libs.utils import print_status
from libs.utils import parse_proxy_file
from libs.proxy_harvester import find_proxies
from libs.attack import report_profile_attack
from libs.attack import report_video_attack

from multiprocessing import Process
from colorama import Fore, Back, Style
import time

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]  # Fixed slicing syntax # Fixed slicing syntax

def profile_attack_process(username, proxy_list):
    try:
        if (len(proxy_list) == 0):
            for _ in range(10):
                try:
                    print_status(f"Attempting to report {username} without proxy...")
                    success = report_profile_attack(username, None)
                    if success:
                        print_success(f"Successfully reported {username}")
                    time.sleep(5)  # Increased delay to 5 seconds
                except Exception as e:
                    print_error(f"Detailed error during report: {type(e).__name__}: {str(e)}")
                    time.sleep(10)  # Add extra delay after errors
            return

        for proxy in proxy_list:
            try:
                print_status(f"Attempting to report {username} using proxy {proxy}...")
                success = report_profile_attack(username, proxy)
                if success:
                    print_success(f"Successfully reported {username} using proxy {proxy}")
                time.sleep(5)  # Increased delay to 5 seconds
            except Exception as e:
                print_error(f"Detailed error with proxy {proxy}: {type(e).__name__}: {str(e)}")
                time.sleep(10)  # Add extra delay after errors
    except Exception as e:
        print_error(f"Process error: {type(e).__name__}: {str(e)}")

def video_attack_process(video_url, proxy_list):
    if (len(proxy_list) == 0):
        for _ in range(10):
            report_video_attack(video_url, None)
        return

    for proxy in proxy_list:
        report_video_attack(video_url, proxy)

def video_attack(proxies):
    video_url = ask_question("Enter the link of the video you want to report")
    print(Style.RESET_ALL)
    if (len(proxies) == 0):
        for k in range(5):
            p = Process(target=video_attack_process, args=(video_url, [],))
            p.start()
            print_status(str(k + 1) + ". Transaction Opened!")
            if (k == 5): print()
        return

    chunk = list(chunks(proxies, 10))

    print("")
    print_status("Video complaint attack is starting!\n")

    i = 1
    for proxy_list in chunk:
        p = Process(target=video_attack_process, args=(video_url, proxy_list,))
        p.start()
        print_status(str(i) + ". Transaction Opened!")
        if (k == 5): print()
        i = i + 1

def profile_attack(proxies):
    k = 0
    username = ask_question("Enter the username of the person you want to report")
    print(Style.RESET_ALL)
    if (len(proxies) == 0):
        for k in range(2):  # Reduced from 5 to 2 concurrent processes
            p = Process(target=profile_attack_process, args=(username, [],))
            p.start()
            print_status(str(k + 1) + ". Transaction Opened!")
            time.sleep(2)  # Add delay between process starts
        return

    chunk = list(chunks(proxies, 10))

    print("")
    print_status("Profile complaint attack is starting!\n")

    i = 1
    for proxy_list in chunk:
        p = Process(target=profile_attack_process, args=(username, proxy_list,))
        p.start()
        print_status(str(i) + ". Transaction Opened!")
        if (k == 5): print()
        i = i + 1

def main():
    print_success("Modules loaded!\n")

    ret = ask_question("Would you like to use a proxy? [Y/N]")

    proxies = []

    if (ret == "Y" or ret == "y"):
        ret = ask_question("Would you like to collect your proxies from the internet? [Y/N]")

        if (ret == "Y" or ret == "y"):
            print_status("Gathering proxy from the Internet! This may take a while.\n")
            proxies = find_proxies()
        elif (ret == "N" or ret == "n"):
            print_status("Please have a maximum of 50 proxies in a file!")
            file_path = ask_question("Enter the path to your proxy list")
            proxies = parse_proxy_file(file_path)
        else:
            print_error("Answer not understood, exiting!")
            exit()

        print_success(str(len(proxies)) + " Number of proxies found!\n")
    elif (ret == "N" or ret == "n"):
        pass
    else:
        print_error("Answer not understood, exiting!")
        exit()

    

    print("")
    print_status("1 - Report the profile.")
    print_status("2 - Report a video.")
    report_choice = ask_question("Please select the complaint method")
    print("")

    if (report_choice.isdigit() == False):
        print_error("The answer is not understood.")
        exit(0)
    
    if (int(report_choice) > 2 or int(report_choice) == 0):
        print_error("The answer is not understood..")
        exit(0)

    if (int(report_choice) == 1):
        profile_attack(proxies)
    elif (int(report_choice) == 2):
        video_attack(proxies)

if __name__ == "__main__":
    print_logo()
    try:
        main()
        print(Style.RESET_ALL)
    except KeyboardInterrupt:
        print("\n\n" + Fore.RED + "[ * ] The program is closing!")
        print(Style.RESET_ALL)
        _exit(0)
