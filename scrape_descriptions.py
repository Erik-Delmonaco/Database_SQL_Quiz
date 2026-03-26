import csv
import requests
import re
from html.parser import HTMLParser
from urllib.parse import quote


class DescriptionParser(HTMLParser):
    """Extracts text content from HTML description."""
    def __init__(self):
        super().__init__()
        self.text = []
        self.in_headline = False
    
    def handle_starttag(self, tag, attrs):
        if tag == 'h2':
            for attr, value in attrs:
                if attr == 'class' and 'title-lc-m' in value:
                    self.in_headline = True
    
    def handle_endtag(self, tag):
        if tag == 'h2':
            self.in_headline = False
    
    def handle_data(self, data):
        if self.in_headline:
            text = data.strip()
            if text:
                self.text.append(text)
    
    def get_text(self):
        return ' '.join(self.text).strip()


def name_to_slug(name: str) -> str:
    """Convert an inductee name to URL slug format."""
    # Handle special cases and convert to lowercase with hyphens
    slug = name.strip().lower()
    # Replace spaces and special characters with hyphens
    slug = re.sub(r'[&\s]+', '-', slug)
    # Remove any remaining special characters
    slug = re.sub(r'[^a-z0-9\-]', '', slug)
    # Remove duplicate hyphens
    slug = re.sub(r'-+', '-', slug)
    return slug


def fetch_description(name: str) -> str | None:
    """Fetch description for an inductee from the Rock & Roll Hall of Fame website."""
    slug = name_to_slug(name)
    url = f"https://rockhall.com/inductees/{slug}/"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            print(f"  ✗ {name}: HTTP {response.status_code}")
            return None
        
        # Extract description from HTML
        parser = DescriptionParser()
        parser.feed(response.text)
        description = parser.get_text()
        
        if description:
            print(f"  ✓ {name}")
            return description
        else:
            print(f"  ? {name}: No description found")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"  ✗ {name}: {e}")
        return None


def update_bio_csv():
    """Read bio.csv, fetch descriptions, and write updated CSV with description column."""
    print("Reading bio.csv...")
    
    # Read existing data
    inductees = []
    with open('bio.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            inductees.append(row)
    
    print(f"Found {len(inductees)} inductees. Fetching descriptions...\n")
    
    # Fetch descriptions
    for inductee in inductees:
        description = fetch_description(inductee['name'])
        inductee['description'] = description if description else ''
    
    # Write updated CSV
    print("\nWriting updated bio.csv...")
    fieldnames = ['name', 'inducted', 'category', 'inducted_by', 'description']
    with open('bio.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(inductees)
    
    print("✓ bio.csv updated successfully!")


if __name__ == '__main__':
    update_bio_csv()
