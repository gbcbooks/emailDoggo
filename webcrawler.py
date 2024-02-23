from html import unescape
from concurrent.futures import ThreadPoolExecutor
from data_store import DataStore
import requests
from bs4 import BeautifulSoup
import re
import threading
import pickle
from urllib.parse import urljoin, urlparse, urlunparse
from time import sleep
from queue import Queue
from requests import Timeout


class WebCrawler:
    def __init__(self, start_url, depth, num_threads, output_file, keywords, domain, user_agent=None, requests_per_second=None,
                 proxy=None, request_timeout=10):
        print(f"Starting crawl at {start_url} with depth {depth} using {num_threads} threads.")
        self.start_url = start_url
        self.depth = depth
        self.visited_urls = set()
        self.thread_pool = []
        self.thread_lock = threading.Lock()
        self.url_queue = Queue()
        self.output_file = output_file
        self.load_excluded_domain(domain)
        self.load_keywords_from_file(keywords) # load keywords
        self.user_agent = user_agent or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
        self.requests_per_second = requests_per_second or 1  # Default rate limiter
        self.proxy = proxy
        self.request_timeout = request_timeout
        self.executor = ThreadPoolExecutor(max_workers=num_threads)
        for _ in range(num_threads):
            self.executor.submit(self.crawl_thread)

        # Database object
        self.data_store = DataStore()

        self.RED = 31
        self.GREEN = 32
        self.YELLOW = 33
        self.BLUE = 34
        self.WHITE = 37
        self.SAVE_FILE = "save.p"

        self.url_queue.put((start_url, 1))

        for _ in range(num_threads):
            thread = threading.Thread(target=self.crawl_thread)
            thread.start()
            self.thread_pool.append(thread)
            print(f"Thread {_ + 1} started.")

    def colored_text(self, text, color_code):
        return f"\033[{color_code}m{text}\033[0m"

    def load_keywords_from_file(self, filename):
        with open(filename, 'r') as file:
            # Reading lines from the file and stripping whitespace
            self.keywords = [line.strip() for line in file.readlines()]

        print(f"Loaded {len(self.keywords)} keywords from {filename}")

    def normalize_url(self, base_url, found_url):
        # Convert relative URL to absolute URL
        absolute_url = urljoin(base_url, found_url)
        # Parse the absolute URL
        parsed_url = urlparse(absolute_url)
        # Remove query parameters and fragments
        normalized_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', '', ''))
        return normalized_url

    def save_state(self, file_name):
        state = {
            'visited_urls': list(self.visited_urls),
            'url_queue': list(self.url_queue.queue),
        }
        with open(file_name, 'wb') as file:
            pickle.dump(state, file)
        print(f"Crawling state saved to {file_name}.")

    def load_state(self, file_name):
        with open(file_name, 'rb') as file:
            state = pickle.load(file)

        self.visited_urls = set(state['visited_urls'])
        for url, depth in state['url_queue']:
            self.url_queue.put((url, depth))

        print(f"Crawling state loaded from {file_name}.")        

    def write_to_file(self, emails):
        with open(self.output_file, 'r') as file:
            emails_set = file.readlines()
        with open(self.output_file, 'a') as file:
            if emails not in emails_set:
                for email in emails:
                    file.write(email + '\n')
                    print(f"Written emssail {email} to file.")
            else:
                print(f"email is exist in {self.output_file}")
                
    def wait_for_completion(self):
        self.executor.shutdown(wait=True)
        print("All threads have completed.")

    def mime_check(self, response, current_url):
        # Check the MIME type of the response
        content_type = response.headers.get('Content-Type', '')
        if 'text/html' not in content_type:
            print(self.colored_text(f"Skipping non-HTML content at {current_url} (MIME type: {content_type})",
                                    self.YELLOW))
            self.url_queue.task_done()
            return True
        return False
    
    def load_excluded_domain(self, filename):
        with open(filename, "r") as file:
            # Reading lines from the file and stripping whitespace
            self.excluded_domain = [line.replace("\n","") for line in file.readlines()]
        print(f"Loaded {len(self.excluded_domain)} keywords from {filename}")
    
    def domain_exclude_check(self, current_url):
        current_domain = urlparse(current_url).netloc
        if current_domain in self.excluded_domain:
            print(f"Skipping {current_domain}. excluded")
            return True
        return False

    def dup_check(self, current_url, current_depth):
        if current_depth > self.depth or current_url in self.visited_urls:
            print(f"Skipping {current_url}.")
            self.url_queue.task_done()
            return True
        return False

    def meta_check(self, soup, current_url, current_depth):
        meta_refresh_tag = soup.find('meta', attrs={'http-equiv': re.compile(r'refresh', re.I)})
        if meta_refresh_tag and 'content' in meta_refresh_tag.attrs:
            content = meta_refresh_tag['content']
            refresh_url = content.split('URL=')[-1] if 'URL=' in content else None
            if refresh_url:
                refresh_url = unescape(refresh_url.strip())
                # Normalize and add the refresh URL to the queue
                normalized_refresh_url = self.normalize_url(current_url, refresh_url)
                print(f"Found meta refresh URL {normalized_refresh_url}. Adding to queue.")
                self.url_queue.put((normalized_refresh_url, current_depth + 1))
                return True  # Skip further processing of the current page
        return False

    def crawl_thread(self):
        while not self.url_queue.empty():

            current_url, current_depth = self.url_queue.get()

            if self.domain_exclude_check(current_url):
                continue
            
            # Check for duplicate urls
            if self.dup_check(current_url, current_depth):
                continue

            with self.thread_lock:
                self.visited_urls.add(current_url)
                print(self.colored_text(f"[i] Scanning {current_url}", self.BLUE))

            # Implementation of User-Agent headers
            headers = {'User-Agent': self.user_agent}

            # Implementation of rate limiter
            sleep(self.requests_per_second)
            try:
                response = requests.get(current_url, headers=headers, proxies=self.proxy, timeout=self.request_timeout, allow_redirects=True)

                # Init mime check
                if self.mime_check(response, current_url):
                    continue

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Meta check
                    if self.meta_check(soup, current_url, current_depth):
                        continue

                    if any(keyword in current_url or keyword in soup.get_text() for keyword in self.keywords):
                        emails = re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', soup.get_text())
                        if emails:
                            self.data_store.insert_emails(emails, current_url)
                            self.write_to_file(emails)
                        for email in emails:
                            print(self.colored_text(f"[+] Email extracted: {email}", self.GREEN))
                            self.save_state(self.SAVE_FILE)
                            

                    for link in soup.find_all('a'):
                        next_url = link.get('href')
                        if next_url:
                            # Remove params
                            next_url = self.normalize_url(current_url, next_url)

                            if next_url.startswith('http'):
                                print(f"Found link {next_url}. Adding to queue.")
                                self.url_queue.put((next_url, current_depth + 1))
                                self.data_store.insert_url(current_url, response.content.decode('utf-8'))
                            elif next_url.startswith('/'):
                                print(f"Found relative link {next_url}. Adding to queue.")
                                self.url_queue.put((current_url + next_url, current_depth + 1))
                                self.data_store.insert_url(current_url, response.content.decode('utf-8'))

            except Timeout:
                print(self.colored_text(f"Request to {current_url} timed out.", self.RED))
            except Exception as e:
                print(self.colored_text(f"Error: {str(e)}", self.RED))

            self.url_queue.task_done()
            print(f"Finished scanning {current_url}.")
