import os

from webcrawler import WebCrawler
from concurrent.futures import ThreadPoolExecutor
from time import sleep
import os
import platform
import argparse


def clear_screen() -> object:
    system = platform.system()
    if system == 'Windows':
        os.system('cls')
    elif system == 'Linux' or system == 'Darwin':  # Unix-like systems (Linux and macOS)
        os.system('clear')
    else:
        print("Clearing screen not supported on this platform.")
    return

def splash():
    doge = """
        ▄              ▄
        ▌▒█           ▄▀▒▌
        ▌▒▒█        ▄▀▒▒▒▐
       ▐▄▀▒▒▀▀▀▀▄▄▄▀▒▒▒▒▒▐
     ▄▄▀▒░▒▒▒▒▒▒▒▒▒█▒▒▄█▒▐
   ▄▀▒▒▒░░░▒▒▒░░░▒▒▒▀██▀▒▌
  ▐▒▒▒▄▄▒▒▒▒░░░▒▒▒▒▒▒▒▀▄▒▒▌
  ▌░░▌█▀▒▒▒▒▒▄▀█▄▒▒▒▒▒▒▒█▒▐
 ▐░░░▒▒▒▒▒▒▒▒▌██▀▒▒░░░▒▒▒▀▄▌
 ▌░▒▄██▄▒▒▒▒▒▒▒▒▒░░░░░░▒▒▒▒▌
▌▒▀▐▄█▄█▌▄░▀▒▒░░░░░░░░░░▒▒▒▐
▐▒▒▐▀▐▀▒░▄▄▒▄▒▒▒▒▒▒░▒░▒░▒▒▒▒▌
▐▒▒▒▀▀▄▄▒▒▒▄▒▒▒▒▒▒▒▒░▒░▒░▒▒▐
 ▌▒▒▒▒▒▒▀▀▀▒▒▒▒▒▒░▒░▒░▒░▒▒▒▌
 ▐▒▒▒▒▒▒▒▒▒▒▒▒▒▒░▒░▒░▒▒▄▒▒▐
  ▀▄▒▒▒▒▒▒▒▒▒▒▒░▒░▒░▒▄▒▒▒▒▌
    ▀▄▒▒▒▒▒▒▒▒▒▒▄▄▄▀▒▒▒▒▄▀
      ▀▄▄▄▄▄▄▀▀▀▒▒▒▒▒▄▄▀
         ▒▒▒▒▒▒▒▒▒▒▀▀
    """

    lines = doge.strip().split('\n')

    for line in lines:
        for char in line:
            print(char, end='', flush=True)
            sleep(0.0005)  # Adjust the delay as needed
        print()
    sleep(2)

    print("\n\n much email \n\t doge happy \n\t\t many client\n\t\t\t wow")
    line = "--------------------------------------------------------------"
    
    for char in line:
        print(char, end='', flush=True)
        sleep(0.003)
    sleep(1)
    clear_screen()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Web Crawler')
    parser.add_argument('--url', '-u', required=True, help='Starting URL')
    parser.add_argument('--depth', '-d', type=int, required=True, help='Depth of crawling')
    parser.add_argument('--threads', '-t', type=int, default=4, help='Number of threads (default: 4)')
    parser.add_argument('--rate-limit', '-r', type=int, default=1, help='Set rate limit for crawler - default: 1 (seconds)')
    parser.add_argument('--load', '-l', help='Loads a previously saved session')
    parser.add_argument('--output', '-o', default='emails.txt', help='Output file for emails (default: emails.txt)')
    parser.add_argument('--user-agent', '-x', default=None, help='Set the user-agent header for requests')
    parser.add_argument('--keywords', '-k', default='keywords.txt', help='Filename for keywords (Default: keywords.txt), left @ means all emails')

    args = parser.parse_args()
    splash()
    crawler = WebCrawler(args.url, args.depth, args.threads, args.output, args.keywords, args.user_agent, args.rate_limit)
    crawler.wait_for_completion()
