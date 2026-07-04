#!/usr/bin/env python3
"""
InstaCPR TUI - Clean Terminal Interface
Uses the new core framework (MetaReporter + Workflow)
"""

from core.models import ReportData
from core.reporter import MetaReporter
import time
import os
from urllib.parse import urlparse
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    clear_screen()
    print("=" * 60)
    print(" " * 20 + "INSTACPR v1.0 - TUI")
    print("=" * 60)
    print()
def normalize_url(url: str) -> str:
    url = url.strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    return url


def validate_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and parsed.netloc != ""
def get_user_input():
    print_header()

    # Platform
    print("Platform:")
    print("  1) Instagram")
    print("  2) Facebook")
    while True:
        choice = input("\nChoose (1/2): ").strip()
        if choice == "1":
            platform = "instagram"
            break
        elif choice == "2":
            platform = "facebook"
            break
        print("Invalid choice.")

    # Full name
    fullname = input("\nFull name: ").strip()
    if not fullname:
        fullname = "User"

    while True:
        copied_url = normalize_url(
            input("Your content URL: ")
        )

        if validate_url(copied_url):
            break

        print("❌ Invalid URL. Please try again.")

    while True:
        target_url = normalize_url(
            input("Target (infringing) URL: ")
        )

        if validate_url(target_url):
            break

        print("❌ Invalid URL. Please try again.")

    # Headless
    headless_choice = input("\nRun headless? [Y/n]: ").strip().lower()
    headless = headless_choice != "n"

    # Proxy (simple for now)
    use_proxy = input("\nUse proxy? [y/N]: ").strip().lower() == "y"
    proxy_config = None

    if use_proxy:
        host = input("Proxy host (IP:PORT): ").strip()
        if host:
            proxy_config = f"http://{host}"

    return platform, fullname, copied_url, target_url, headless, proxy_config

def main():
    print_header()
    print("Welcome to InstaCPR Terminal Interface")
    print("Using the new core framework.\n")

    platform, fullname, copied_url, target_url, headless, proxy_config = get_user_input()

    report = ReportData(
        platform=platform,
        fullname=fullname,
        copied_url=copied_url,
        target_url=target_url,
    )

    print("\n" + "="*60)
    print("Starting Report")
    print("="*60)
    print(f"Platform : {platform.title()}")
    print(f"Name     : {fullname}")
    print(f"Headless : {headless}")
    print(f"Proxy    : {'Enabled' if proxy_config else 'Disabled'}")
    print("="*60)
    input("\nPress ENTER to start the report...")

    def progress_callback(text: str):
        print(f"→ {text}")

    reporter = MetaReporter(
        report_data=report,
        proxy_config=proxy_config,
        headless=headless,
        progress_callback=progress_callback
    )

    try:
        reporter.run()
        print("\n🎉 Report completed successfully!")
    except Exception as e:
        print(f"\n❌ Report failed: {e}")

    input("\nPress ENTER to exit...")

if __name__ == "__main__":
    main()