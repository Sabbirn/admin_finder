import requests
import sys
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor

# Predefined admin panel paths (Add more as needed)
ADMIN_PATHS = [
    "admin/", "administrator/", "adminpanel/", "login/", "dashboard/", "admin/login/",
    "controlpanel/", "manage/", "cms/", "admin.php", "admin.html", "admin/index.php",
    "wp-admin/", "backend/", "panel/", "member/", "users/", "account/", "login/admin/",
    "server/", "system/", "management/", "root/", "adminarea/", "admin_area/", "secure/",
    "access/", "adm/", "useradmin/", "securearea/", "superadmin/", "cpanel/", "control/",
    "login.php", "portal/", "adminportal/", "webadmin/", "admin123/", "login_admin/",
    # Extend to 1000 entries with additional paths
] + [f"admin{num}/" for num in range(1, 1001)]  # Generate paths dynamically up to 1000

# Colors for better readability in Termux
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def check_admin_panel(base_url, path):
    """Check if a specific admin panel path is active."""
    url = urljoin(base_url, path)
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"{Colors.OKGREEN}[FOUND] {url}{Colors.ENDC}")
            return url
        else:
            print(f"{Colors.WARNING}[NOT FOUND] {url} - Status: {response.status_code}{Colors.ENDC}")
    except requests.RequestException as e:
        print(f"{Colors.FAIL}[ERROR] {url} - {e}{Colors.ENDC}")
    return None

def find_admin_panels(base_url):
    """Scan for active admin panels using multiple threads."""
    print(f"{Colors.HEADER}Scanning {base_url} for admin panels...{Colors.ENDC}")

    # Ensure the URL starts with http:// or https://
    if not base_url.startswith(("http://", "https://")):
        base_url = "http://" + base_url

    active_panels = []

    with ThreadPoolExecutor(max_workers=20) as executor:
        results = executor.map(lambda path: check_admin_panel(base_url, path), ADMIN_PATHS)
        active_panels = [result for result in results if result is not None]

    return active_panels

def main():
    print(f"{Colors.BOLD}Welcome to the Advanced Admin Panel Finder!{Colors.ENDC}")

    # Accept base URL input
    base_url = input(f"{Colors.OKBLUE}Enter the target website URL (e.g., http://example.com): {Colors.ENDC}").strip()
    if not base_url:
        print(f"{Colors.FAIL}Error: URL cannot be empty. Exiting.{Colors.ENDC}")
        sys.exit(1)

    # Start scanning
    active_panels = find_admin_panels(base_url)

    # Display results
    if active_panels:
        print(f"{Colors.OKGREEN}\nActive admin panels found:{Colors.ENDC}")
        for panel in active_panels:
            print(f" - {panel}")
    else:
        print(f"{Colors.FAIL}\nNo active admin panels found.{Colors.ENDC}")

if __name__ == "__main__":
    main()
