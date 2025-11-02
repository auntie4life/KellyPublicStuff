# WordPress Blog Text Scraper

A Python script that extracts text content from WordPress blog posts and saves them as individual text files. Perfect for backing up or migrating blog content!

## What It Does

This script will:
- Discover all blog posts on a WordPress site
- Extract just the text content from each post (no images, headers, footers, or navigation)
- Remove social sharing buttons and comments
- Save each post as a separate `.txt` file with the title, date, URL, and clean text content

## Requirements

- Python 3.6 or higher
- Internet connection
- A WordPress blog with standard URL structure (like `yourblog.com/2024/01/15/post-title/`)

## Step-by-Step Installation

### Step 1: Install Python

**Windows:**
1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download the latest Python 3 installer (e.g., Python 3.12)
3. Run the installer
4. ✅ **IMPORTANT:** Check the box "Add Python to PATH" at the bottom of the installer
5. Click "Install Now"
6. Wait for installation to complete

**Mac:**
1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download the latest Python 3 installer
3. Open the downloaded `.pkg` file and follow the installation steps

**To verify Python is installed:**
Open Terminal (Mac) or PowerShell (Windows) and type:
```bash
python --version
```
You should see something like: `Python 3.12.0`

### Step 2: Install Required Python Libraries

Open PowerShell (Windows) or Terminal (Mac) and run these commands one at a time:

```bash
pip install requests
```

```bash
pip install beautifulsoup4
```

```bash
pip install lxml
```

**Alternative (all at once):**
```bash
pip install requests beautifulsoup4 lxml
```

**If you get an error like "pip is not recognized"**, try:
```bash
python -m pip install requests beautifulsoup4 lxml
```

**On Mac, if you get permission errors**, try:
```bash
pip install requests beautifulsoup4 lxml --user
```

### Step 3: Configure the Script for Your Blog

1. Open `wordpress_scraper.py` in a text editor (Notepad, TextEdit, VS Code, etc.)
2. Find line 22 that says:
   ```python
   BASE_URL = "https://yourblog.com/"
   ```
3. Replace `https://yourblog.com/` with your actual blog URL
4. Make sure to keep the quotes and the trailing slash `/`
5. Save the file

**Example:**
```python
BASE_URL = "https://myblog.wordpress.com/"
```

## Usage

### Basic Usage

1. Put the script (`wordpress_scraper.py`) in a folder where you want the posts saved
2. Open PowerShell or Command Prompt in that folder
3. Run:
   ```bash
   python wordpress_scraper.py
   ```

### What Happens

The script will:
1. **Discover posts** - Either via sitemap (fast) or by crawling the site (slower)
2. **Extract content** - Process each post one at a time
3. **Save files** - Create an `exported_posts` folder with one `.txt` file per post

### Output

Files are saved in the `exported_posts` folder with names like:
- `0001_Post_Title.txt`
- `0002_Another_Post_Title.txt`
- `0003_Yet_Another_Post.txt`

Each file contains:
```
Title: [Post Title]
Date: [Publication Date]
URL: [Original URL]

================================================================================

[Clean text content of the post]
```

## Customizing for Different Blogs

The script is already configured to work with most WordPress blogs. To use it on a different blog:

1. Open `wordpress_scraper.py` in a text editor
2. Find line 22: `BASE_URL = "https://yourblog.com/"`
3. Change it to the new blog's URL
4. Save and run the script again

## What to Expect

### Speed
- With sitemap: ~1-2 seconds per post
- Without sitemap (crawling): 2-5 minutes to discover posts, then ~1-2 seconds per post
- For 100 posts: expect about 2-5 minutes total

### Warnings You Might See

**⚠ "Could not find content div, trying body"**
- This is normal! It means the post has a different HTML structure
- The script will still extract the content correctly
- Common for older posts or if the blog changed themes

**❌ "Failed to extract content"**
- Rare, but can happen if a post is password-protected or has unusual formatting
- The script will skip that post and continue with the rest

## Troubleshooting

### "pip is not recognized"
Try:
```bash
python -m pip install requests beautifulsoup4 lxml
```

### "python is not recognized"
Make sure Python is installed and added to your PATH. Try:
```bash
py wordpress_scraper.py
```

### Script runs but files are empty or very short
The blog's HTML structure might be different. The script works best with standard WordPress themes.

### Too many "Failed to extract content" errors
The blog might:
- Use a non-standard WordPress theme
- Have password-protected posts
- Block automated requests

## Script Features

### What Gets Removed
- Images and embedded media
- Social sharing buttons ("Share this", "Tweet", etc.)
- Comments and comment forms
- Navigation menus
- Sidebars and widgets
- Headers and footers
- Related posts

### What Gets Kept
- Post title
- Publication date
- Main text content
- Original URL for reference

### URL Filtering
The script only extracts posts with standard WordPress URLs like:
- `https://blog.com/2017/06/21/post-title/`

It automatically skips:
- Image attachment pages
- Category/tag archives
- Author pages
- Search results
- About/contact pages

## Technical Details

- Uses BeautifulSoup4 for HTML parsing
- Polite scraping: 1-second delay between requests
- Handles both sitemap and crawling methods
- Validates dates and URL structure
- Creates safe filenames from post titles

## Tips

1. **Run overnight for large blogs** - If you have 500+ posts, consider running it before bed
2. **Check a few files first** - After it processes 5-10 posts, press Ctrl+C and check if the output looks good
3. **Keep the originals** - This extracts text only, so keep your WordPress export XML as a backup
4. **Restart is OK** - If interrupted, just run the script again - it will overwrite existing files

## Limitations

- Text only - doesn't save images or videos
- Requires valid WordPress URL structure (won't work on all custom blogs)
- No incremental updates - processes all posts each time
- May not work perfectly on heavily customized WordPress themes

## License

Free to use and modify for personal projects.

## Questions?

If the script isn't working for your blog, the issue is usually:
1. The blog doesn't use standard WordPress URL structure
2. The blog blocks automated access
3. Need to adjust the content extraction selectors for that specific theme

---

**Works with:** Most standard WordPress blogs  
**Last updated:** November 2025
