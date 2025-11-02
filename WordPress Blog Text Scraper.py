#!/usr/bin/env python3
"""
WordPress Blog Text Scraper - Improved Version

This script crawls a WordPress blog and extracts the text content from each post,
saving them as individual text files.

Usage:
    python wordpress_scraper.py

Requirements:
    pip install requests beautifulsoup4 lxml
"""

import requests
from bs4 import BeautifulSoup
import re
import os
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse


# Configuration
BASE_URL = "https://insearchofthevery.com/"
OUTPUT_DIR = "exported_posts"
DELAY_BETWEEN_REQUESTS = 1  # Be polite to the server (seconds)


def sanitize_filename(filename):
    """Create a safe filename from post title."""
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    filename = re.sub(r'[\s]+', '_', filename)
    filename = re.sub(r'_+', '_', filename)
    if len(filename) > 200:
        filename = filename[:200]
    return filename.strip('_')


def is_valid_post_url(url, base_url):
    """Check if URL is a valid blog post."""
    url = url.split('#')[0].split('?')[0]
    parsed = urlparse(url)
    path = parsed.path.rstrip('/')
    
    if not url.startswith(base_url) or path in ['/', '']:
        return False
    
    path_parts = [p for p in path.split('/') if p]
    
    if len(path_parts) != 4:
        return False
    
    try:
        year = int(path_parts[0])
        month = int(path_parts[1])
        day = int(path_parts[2])
        
        if not (2000 <= year <= 2030) or not (1 <= month <= 12) or not (1 <= day <= 31):
            return False
    except ValueError:
        return False
    
    post_slug = path_parts[3].lower()
    image_patterns = [
        r'^fb_img', r'^\d{8}_\d{6}$', r'^img[_-]?\d+', r'^dsc[_-]?\d+',
        r'^\d{4}-\d{2}-\d{2}', r'^screenshot', r'^image[_-]?\d*', r'^\d+$',
    ]
    
    for pattern in image_patterns:
        if re.match(pattern, post_slug):
            return False
    
    return True


def get_all_post_urls(base_url, max_pages=100):
    """Discover all blog post URLs."""
    print(f"Discovering blog posts from {base_url}...\n")
    
    discovered_urls = set()
    
    # Try sitemap first
    sitemap_urls = [
        urljoin(base_url, 'sitemap.xml'),
        urljoin(base_url, 'sitemap_index.xml'),
        urljoin(base_url, 'wp-sitemap.xml'),
    ]
    
    for sitemap_url in sitemap_urls:
        try:
            response = requests.get(sitemap_url, timeout=10)
            if response.status_code == 200 and 'xml' in response.headers.get('content-type', ''):
                soup = BeautifulSoup(response.content, 'xml')
                for loc in soup.find_all('loc'):
                    url = loc.text.strip().split('#')[0].split('?')[0]
                    if is_valid_post_url(url, base_url):
                        discovered_urls.add(url)
                
                if discovered_urls:
                    print(f"✓ Found {len(discovered_urls)} posts via sitemap!")
                    return sorted(list(discovered_urls))
        except Exception:
            pass
    
    # Fallback to crawling
    print("No sitemap found, crawling site...\n")
    pages_to_check = [base_url]
    checked_pages = set()
    
    while pages_to_check and len(checked_pages) < max_pages:
        current_page = pages_to_check.pop(0)
        
        if current_page in checked_pages:
            continue
        
        checked_pages.add(current_page)
        print(f"Checking: {current_page}")
        
        try:
            response = requests.get(current_page, timeout=10)
            if response.status_code != 200:
                continue
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            for link in soup.find_all('a', href=True):
                url = urljoin(base_url, link['href']).split('#')[0].split('?')[0]
                
                if is_valid_post_url(url, base_url):
                    discovered_urls.add(url)
                
                if url.startswith(base_url) and url not in checked_pages:
                    if '/page/' in url or url == base_url:
                        pages_to_check.append(url)
            
            time.sleep(DELAY_BETWEEN_REQUESTS)
            
        except Exception as e:
            print(f"  Error: {e}")
            continue
    
    print(f"\n✓ Discovered {len(discovered_urls)} blog posts!")
    return sorted(list(discovered_urls))


def extract_post_content(url):
    """Extract the main content from a blog post."""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return None
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title
        title = None
        title_elem = soup.find('h1', class_='entry-title')
        if not title_elem:
            title_elem = soup.find('h1')
        if title_elem:
            title = title_elem.get_text(strip=True)
        
        if not title:
            title_elem = soup.find('title')
            if title_elem:
                title = title_elem.get_text(strip=True)
                title = re.split(r'[|–-]', title)[0].strip()
        
        # Extract date
        date = None
        date_elem = soup.find('time', class_='entry-date')
        if not date_elem:
            date_elem = soup.find('time')
        if date_elem:
            date = date_elem.get_text(strip=True)
        
        # Find the main post content
        # WordPress.com uses entry-content class
        content_div = soup.find('div', class_='entry-content')
        
        if not content_div:
            # Try alternative selectors
            content_div = soup.find('article')
            if content_div:
                # Remove header/footer from article
                for elem in content_div.find_all(['header', 'footer']):
                    elem.decompose()
        
        if not content_div:
            content_div = soup.find('main')
        
        if not content_div:
            print("  ⚠ Could not find content div, trying body")
            content_div = soup.find('body')
        
        if not content_div:
            return None
        
        # Make a copy to work with
        content_copy = BeautifulSoup(str(content_div), 'html.parser')
        
        # Remove specific unwanted elements from the copy
        unwanted_selectors = [
            'script', 'style', 'nav', 'aside', 'iframe', 'form',
            '.sharedaddy', '.share-buttons', '.sd-sharing',
            '#comments', '.comments-area', '.comment-respond',
            '.related-posts', '.jp-relatedposts',
            '.widget', '.sidebar', '.navigation', '.post-navigation',
        ]
        
        for selector in unwanted_selectors:
            for element in content_copy.select(selector):
                element.decompose()
        
        # Get text with proper spacing
        text = content_copy.get_text(separator='\n', strip=True)
        
        # Clean up common WordPress patterns
        text = re.sub(r'Share this:.*?(?=\n\n|\Z)', '', text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'Click to (share|email|print).*?(?=\n)', '', text, flags=re.IGNORECASE)
        text = re.sub(r'(Facebook|Twitter|Pinterest|Email|Print|LinkedIn|Tumblr|Reddit|WhatsApp|Pocket|Telegram|Skype)\n', '', text)
        text = re.sub(r'Posted in.*?\nTagged.*?\n', '', text)
        text = re.sub(r'Leave a (comment|reply).*?\n', '', text, flags=re.IGNORECASE)
        text = re.sub(r'^Related$', '', text, flags=re.MULTILINE)
        
        # Clean up whitespace
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
        text = text.strip()
        
        return {
            'title': title or "Untitled",
            'date': date or "No date",
            'url': url,
            'content': text
        }
        
    except Exception as e:
        print(f"  Error extracting content: {e}")
        return None


def scrape_blog(base_url, output_dir):
    """Main function to scrape all blog posts."""
    Path(output_dir).mkdir(exist_ok=True)
    
    post_urls = get_all_post_urls(base_url)
    
    if not post_urls:
        print("\n❌ No blog posts found!")
        return
    
    print(f"\nExtracting content from {len(post_urls)} posts...")
    print(f"Saving to '{output_dir}/' directory\n")
    print("=" * 80)
    
    successful = 0
    failed = 0
    
    for i, url in enumerate(post_urls, 1):
        print(f"\n[{i}/{len(post_urls)}] {url}")
        
        post_data = extract_post_content(url)
        
        if not post_data or not post_data['content']:
            print("  ❌ Failed to extract content")
            failed += 1
            continue
        
        safe_title = sanitize_filename(post_data['title'])
        filename = f"{i:04d}_{safe_title}.txt"
        filepath = os.path.join(output_dir, filename)
        
        output_content = f"""Title: {post_data['title']}
Date: {post_data['date']}
URL: {post_data['url']}

{'=' * 80}

{post_data['content']}
"""
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(output_content)
            print(f"  ✓ Saved: {filename} ({len(post_data['content'])} chars)")
            successful += 1
        except Exception as e:
            print(f"  ❌ Error saving: {e}")
            failed += 1
        
        time.sleep(DELAY_BETWEEN_REQUESTS)
    
    print("\n" + "=" * 80)
    print(f"\n✓ DONE!")
    print(f"  Successfully extracted: {successful} posts")
    if failed > 0:
        print(f"  Failed: {failed} posts")
    print(f"  Files saved to: {output_dir}/")


def main():
    print("WordPress Blog Text Scraper")
    print("=" * 80)
    print(f"Target: {BASE_URL}")
    print(f"Output: {OUTPUT_DIR}/")
    print("=" * 80)
    print()
    
    try:
        scrape_blog(BASE_URL, OUTPUT_DIR)
    except KeyboardInterrupt:
        print("\n\n⚠ Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
