# emailDoggo - the email fetcher


## Overview

This script is a multi-threaded web crawler designed to traverse websites and extract specific information based on provided keywords. It's tailored for crawling with the capability to search for specific terms and extract email addresses if they are found on the page.

## Prerequisites

- Python 3.x
- `requests` library
- `BeautifulSoup` library

## Installation

1. Clone the repository or download the script to your local machine.
2. Install the required Python packages using the following command:

   ```bash
   pip install requests beautifulsoup4
   ```

## Usage

Example usage: 

```
python3 main.py -u "https://thehackernews.com" -d 20000 -t 4 -k Malware Ransomware Phishing Spyware Trojan Virus Worm Firewall Encryption Cryptography Authentication Authorization VPN DoS DDoS SIEM SSL TLS Compliance SOC GDPR HIPAA PCI Encryption Breach Privacy Risk Vulnerability Patch Insurance
```

## Contributing

If you'd like to contribute or report issues, please open an issue or pull request on the GitHub repository.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Legal Disclaimer

This web crawling script ("Software") is provided for educational, informational, and research purposes only. By using this Software, you agree to the following terms and conditions:

1. **Compliance with Laws:** You must comply with all applicable local, state, national, and international laws, regulations, and rules related to your use of the Software. This includes, but is not limited to, data protection and privacy laws, intellectual property laws, and computer crime laws.

2. **Ethical Use:** You agree to use the Software in an ethical manner, respecting the rights, privacy, and terms and conditions of the websites you are accessing.

3. **No Unauthorized Access:** You must obtain proper authorization and consent from the owners or administrators of the websites you intend to crawl. Unauthorized access, use, or interference with systems, networks, or data may lead to criminal or civil liability.

4. **No Warranty:** The Software is provided "as is" without any warranties of any kind, either expressed or implied, including but not limited to the implied warranties of merchantability, fitness for a particular purpose, or non-infringement.

5. **Limitation of Liability:** The author(s) and contributor(s) of the Software shall not be liable for any damages, including but not limited to direct, indirect, incidental, consequential, or punitive damages, arising out of or related to your use or inability to use the Software.

6. **Indemnification:** You agree to indemnify, defend, and hold harmless the author(s), contributor(s), and other associated parties from and against all claims, losses, expenses, damages, and costs, including reasonable attorneys' fees, resulting from or related to your violation of this disclaimer or misuse of the Software.

7. **Third-Party Websites:** The Software may contain links or references to third-party websites. Such links are provided for convenience only, and the author(s) and contributor(s) of the Software do not endorse, control, or assume responsibility for the content or practices of these third-party sites.

8. **Modification and Termination:** The author(s) and contributor(s) reserve the right to modify or terminate the Software at any time without notice. Continued use of the Software following any modification constitutes your acceptance of the changes.

9. **No Illegal Use:** You may not use the Software for any illegal or unauthorized purposes, including but not limited to the unauthorized collection, storage, or dissemination of personal or sensitive information.

By accessing or using the Software, you represent and warrant that you have read, understood, and agree to be bound by this legal disclaimer. If you do not agree with any part of this disclaimer, you must immediately cease all use of the Software.
