import requests
from bs4 import BeautifulSoup
import socks
import socket
import sys
from colorama import Fore, Style  # For colored output

# Configure Tor connection
def configure_tor():
    try:
        # Set up Tor proxy
        socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
        socket.socket = socks.socksocket

        # Test Tor connection
        test_url = "https://check.torproject.org"
        response = requests.get(test_url)

        # Check if Tor is working
        if "Congratulations. This browser is configured to use Tor." in response.text:
            print(Fore.GREEN + "[+] Tor is working properly." + Style.RESET_ALL)
        else:
            print(Fore.RED + "[-] Tor is not working properly. Please check your Tor configuration." + Style.RESET_ALL)
            sys.exit(1)
    except Exception as e:
        print(Fore.RED + f"[-] Error configuring Tor: {e}" + Style.RESET_ALL)
        sys.exit(1)

# Common keywords for threat intelligence
COMMON_KEYWORDS = [
    "ransomware", "malware", "phishing", "botnet", "exploit",
    "data breach", "zero-day", "cyber attack", "dark web", "hacking",
    "cryptojacking", "APT", "DDoS", "spyware", "trojan"
]

def check_onion_status(onion_url):
    """
    Check if an onion link is active or dead.
    """
    try:
        response = requests.get(onion_url, timeout=10)
        if response.status_code == 200:
            return Fore.GREEN + "Active" + Style.RESET_ALL
        else:
            return Fore.RED + "Dead" + Style.RESET_ALL
    except:
        return Fore.RED + "Dead" + Style.RESET_ALL

def search_hidden_services(keyword):
    query_url = f"http://ahmia.fi/search/?q={keyword}"
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.get(query_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []

        for result in soup.find_all('li', class_='result'):
            title = result.find('h4').text.strip() if result.find('h4') else "No title"
            description = result.find('p').text.strip() if result.find('p') else "No description"
            onion_link = result.find('cite').text.strip() if result.find('cite') else "No onion link"
            last_seen = result.find('span', class_='lastSeen').text.strip() if result.find('span', class_='lastSeen') else "Unknown"

            # Construct full onion URL
            full_onion_url = f"http://{onion_link}"

            # Check current status
            current_status = check_onion_status(full_onion_url)

            # Append result
            results.append({
                "title": title,
                "description": description,
                "onion_link": full_onion_url,
                "last_seen": last_seen,
                "current_status": current_status
            })

        return results
    except Exception as e:
        print(Fore.RED + f"[-] Error fetching results: {e}" + Style.RESET_ALL)
        return []

def suggest_keywords():
    print("Suggested keywords for threat intelligence:")
    for i, keyword in enumerate(COMMON_KEYWORDS, 1):
        print(f"{i}. {keyword}")
    print()

if __name__ == "__main__":
    # Configure Tor
    configure_tor()

    # Suggest common keywords
    suggest_keywords()

    # Ask user for keyword
    keyword = input("Enter a keyword (e.g., ransomware): ").strip()

    # Search for hidden services
    hidden_services = search_hidden_services(keyword)

    # Display results
    if hidden_services:
        print("\nDiscovered Hidden Services:\n")
        for service in hidden_services:
            print(f"Title: {service['title']}")
            print(f"Description: {service['description']}")
            print(f"Onion Link: {service['onion_link']}")
            print(f"Last Seen: {service['last_seen']}")
            print(f"Current Status: {service['current_status']}")
            print("-" * 50)
    else:
        print(Fore.RED + "No results found." + Style.RESET_ALL)
