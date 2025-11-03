# WordPress Blog Text Extractor - Complete Guide

A collection of Python scripts to extract text content from WordPress blogs and save them as individual text files. Perfect for backing up, archiving, or migrating blog content!

## What This Does

Extract all text content from WordPress blog posts:
- ✅ Just the text - no images, headers, footers, or navigation
- ✅ Removes social sharing buttons and comments  
- ✅ One `.txt` file per blog post
- ✅ Includes title, date, URL, and clean text content
- ✅ Creates a master index CSV file for easy reference
- ✅ Chronologically sorted from oldest to newest

> **⚠️ CRITICAL:** When exporting from WordPress, you must select **"Posts"** (your blog entries), NOT "Pages" (static pages like About/Contact). This is the most common mistake! See the export instructions below for details.

## Two Methods Available

### Method 1: XML Export Parser (RECOMMENDED)
**Best for:** Getting ALL posts from any time period (works for 825+ posts)

**Pros:**
- Gets every published post from the entire blog history
- Handles large blogs efficiently
- More reliable and complete

**Cons:**
- Requires exporting XML file from WordPress first
- XML file can be very large (50-100MB+)

### Method 2: Web Scraper
**Best for:** Recent posts or smaller blogs (<100 posts)

**Pros:**
- No WordPress login needed
- Works directly on public blog

**Cons:**
- Only gets recent posts (typically ~100 most recent)
- Slower than XML method
- May miss older archived posts

---

## Installation

### Step 1: Install Python

**Windows:**
1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download the latest Python 3 installer (e.g., Python 3.12)
3. Run the installer
4. ✅ **CRITICAL:** Check "Add Python to PATH" at the bottom
5. Click "Install Now"

**Mac:**
1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download and install Python for macOS

**Verify installation:**
```bash
python --version
```
Should show: `Python 3.x.x`

### Step 2: Install Required Libraries

Open PowerShell (Windows) or Terminal (Mac) and run:

```bash
pip install requests beautifulsoup4 lxml
```

**If that doesn't work, try:**
```bash
python -m pip install requests beautifulsoup4 lxml
```

**On Mac with permission errors:**
```bash
pip install requests beautifulsoup4 lxml --user
```

---

## Method 1: XML Export Parser (RECOMMENDED)

### Step 1: Export Your Blog

1. Log into WordPress.com
2. Go to **Tools → Export**
3. **CRITICAL:** Select **Posts** (NOT "All content" and NOT "Pages")
   - Posts = Your blog entries (the 825 items you want) ✅
   - Pages = Static pages like "About", "Contact" (you don't want these) ❌
4. Set date range (e.g., October 2016 to November 2025)
5. Click **"Download Export File"**
6. Save the XML file (will be named like `yourblog.WordPress.2025-11-02.xml`)

### Step 2: Run the Parser

Place `wordpress_xml_parser_with_dates.py` in the same folder as your XML file.

Open PowerShell/Terminal in that folder and run:

```bash
python wordpress_xml_parser_with_dates.py yourblog.WordPress.2025-11-02.xml
```

**Example:**
```bash
cd C:\Users\YourName\Downloads
python wordpress_xml_parser_with_dates.py myblog.WordPress.2025-11-02.xml
```

### What You'll Get

The script creates an `exported_posts` folder containing:

**Individual post files** named like:
- `2016-10-09_0001_First_Blog_Post.txt`
- `2017-06-21_0150_Sleep_Is_Overrated.txt`
- `2025-11-01_0825_Latest_Post.txt`

**Master index file:** `_INDEX_ALL_POSTS.csv`
- Open in Excel or Google Sheets
- Columns: Number, Date, Title, Filename, URL
- Sortable and searchable

**Each text file contains:**
```
Title: Post Title Here
Date: Mon, 15 Jan 2024 10:30:00 +0000
URL: https://yourblog.com/2024/01/15/post-title/

================================================================================

[Clean text content with no HTML, images, or formatting]
```

### Processing Time

- **100 posts:** ~10-20 seconds
- **500 posts:** ~30-60 seconds
- **1000+ posts:** ~1-2 minutes

You'll see progress messages every 100 items processed.

---

## Method 2: Web Scraper

### Configure the Script

1. Open `wordpress_scraper.py` in a text editor
2. Find line 22:
   ```python
   BASE_URL = "https://yourblog.com/"
   ```
3. Replace with your actual blog URL
4. Save the file

### Run the Scraper

```bash
python wordpress_scraper.py
```

The script will:
1. Try to find a sitemap (fast)
2. If no sitemap, crawl the blog page by page (slower)
3. Extract text from each post found
4. Save to `exported_posts` folder

### Limitations

- May only get recent posts (~100 most recent)
- Takes longer (1-2 seconds per post)
- Older posts may not be accessible via homepage pagination

---

## File Organization

After running either script, you'll have:

```
exported_posts/
├── _INDEX_ALL_POSTS.csv          ← Master list of all posts
├── 2016-10-09_0001_First_Post.txt
├── 2016-10-15_0002_Second_Post.txt
├── 2016-10-20_0003_Third_Post.txt
├── ...
└── 2025-11-01_0825_Latest_Post.txt
```

**Files are sorted chronologically** from oldest (2016) to newest (2025).

---

## Optional: Generate Visual PDF Archive

After extracting text files, you can optionally create beautifully formatted PDF versions of your blog posts using the companion **PDF Generator** tool.

### Why Generate PDFs?

**You already have complete text backups**, so PDFs are optional. But they offer:
- 📄 **Visual preservation** - Maintains look and layout, includes images
- 📖 **Better reading experience** - Formatted for screen/print with proper styling
- 💾 **Offline collection** - Portable archive for reading anywhere
- 🔍 **Complementary format** - Use text files for searching, PDFs for viewing

### Prerequisites

Install additional dependencies:

```bash
pip install playwright pandas openpyxl beautifulsoup4
```

```bash
playwright install chromium
```

(This downloads a ~170MB headless browser)

### Setup PDF Generator

**Step 1: Prepare URL list**

The XML parser already created `_INDEX_ALL_POSTS.csv` with all your URLs:
1. Open `_INDEX_ALL_POSTS.csv` in Excel
2. Save as `_INDEX_ALL_POSTS.xlsx` (Excel format)

**Step 2: Download the script**

Download `make_printfriendly_pdfs_v2.py`

**Step 3: Configure the path**

Edit line 9 in the script:
```python
XLSX_PATH = r"C:\Users\YourName\Downloads\exported_posts\_INDEX_ALL_POSTS.xlsx"
```

**Windows example:**
```python
XLSX_PATH = r"C:\Users\Kelly\Downloads\1-ISOTV\exported_posts\_INDEX_ALL_POSTS.xlsx"
```

### Run PDF Generator

```bash
python make_printfriendly_pdfs_v2.py
```

### What to Expect

**Progress output:**
```
================================================================================
📁 Output folder: C:\Users\...\PDFs_2025-11-03_03-48-48
📊 Total URLs: 825
⏱️  Timeouts: Nav=90.0s, PDF=90.0s
================================================================================

[1/825] https://yourblog.com/2016/10/09/first-blog-post/
  → Loading page (attempt 1)...
  → Extracting content (simple method)...
  → Generating PDF...
  ✅ Success! (simple method)
```

**Time required:**
- ~3-5 seconds per URL
- 825 posts = **60-90 minutes total**
- Plan to let it run overnight

**Output:**
- New folder: `PDFs_[timestamp]/` with all PDFs
- Log file: `export_log.csv` with status of each URL

**Requirements:**
- Blog must be online and accessible
- Internet connection required
- ~1-2GB disk space for 825 PDFs

### PDF Generator vs Text Extraction

| Feature | Text Files | PDF Files |
|---------|-----------|-----------|
| **Completeness** | ✅ Full content | ✅ Full content |
| **Speed** | Very fast (minutes) | Slower (1-2 hours) |
| **File size** | Tiny (~5KB each) | Larger (~500KB-2MB each) |
| **Images** | Not included | ✅ Included |
| **Formatting** | Plain text | ✅ Visual layout preserved |
| **Searchability** | Perfect | Good |
| **Requires blog online** | No (uses XML backup) | Yes |
| **Best for** | Backup, searching, migration | Reading, printing, visual archive |

**Recommendation:** You already have complete text backups from the XML extraction. PDFs are a nice bonus for visual preservation, but not essential. Generate them if you want a beautiful reading collection or print archive.

For complete PDF generator documentation, see `README_PDF_GENERATOR.md`.

---

## Troubleshooting

### "python is not recognized"
- Python not installed correctly or not in PATH
- Try using `py` instead: `py wordpress_xml_parser_with_dates.py file.xml`
- Reinstall Python and check "Add to PATH"

### "pip is not recognized"
```bash
python -m pip install requests beautifulsoup4 lxml
```

### XML Parser Found 0 Posts
- Make sure you exported **Posts** (not Pages or "All content")
- Posts = Blog entries with dates (what you want)
- Pages = Static pages like About/Contact (not what you want)
- Check that the XML file isn't corrupted
- Run the diagnostic: `python xml_analyzer.py yourfile.xml`

### Web Scraper Only Gets ~100 Posts
- This is expected for blogs with long history
- **Use Method 1 (XML Export)** instead to get all posts

### "Could not find content div, trying body" (yellow warning)
- This is normal for older posts with different themes
- Posts will still be extracted correctly
- The warning is just informational

### Empty or Very Short Text Files
- The post might be password-protected
- The post might only contain images
- The WordPress theme might use non-standard HTML

### File Names Too Long (Windows Error)
- Windows has a 260 character path limit
- Post titles that are very long get truncated automatically
- Files will still be created with shortened names

---

## Understanding the Output

### Filename Format
`YYYY-MM-DD_####_Post_Title.txt`

- **YYYY-MM-DD:** Publication date
- **####:** Sequential number (0001-0825)
- **Post_Title:** Sanitized post title (spaces → underscores, special chars removed)

### CSV Index Columns
1. **Number:** Sequential post number
2. **Date:** Publication date (YYYY-MM-DD)
3. **Title:** Full post title
4. **Filename:** Name of the text file
5. **URL:** Original blog post URL

### Text File Contents
- **Header:** Title, Date, URL
- **Separator:** 80 equals signs
- **Body:** Clean text with:
  - Paragraphs preserved
  - No HTML tags
  - No images or embedded media
  - No social sharing buttons
  - No comments
  - No navigation menus

---

## What Gets Removed

✂️ **Automatically filtered out:**
- Images and videos
- Social sharing buttons ("Share on Facebook", etc.)
- Comments and comment forms
- Navigation menus
- Sidebars and widgets
- Headers and footers
- Related posts
- Advertisement blocks
- Image attachment pages
- Draft posts
- Private posts

✅ **What's kept:**
- Post title
- Publication date
- Main text content
- Original URL (for reference)

---

## Advanced Usage

### Customize Output Directory

Edit the script to change where files are saved:
```python
OUTPUT_DIR = "my_blog_backup"  # Default is "exported_posts"
```

### Process Only Specific Date Range

When exporting from WordPress:
- Set **Start date** and **End date** to limit the date range
- Useful for incremental backups

### Handling Very Large Blogs (2000+ posts)

The XML parser can handle any size:
- 1000 posts: ~2-3 minutes
- 5000 posts: ~10-15 minutes
- 10000 posts: ~30 minutes

Just let it run - progress is shown every 100 items.

---

## Technical Details

### Supported WordPress Versions
- WordPress.com (hosted)
- Self-hosted WordPress with standard export format
- Works with any WordPress blog using standard URL structure

### URL Format Requirements (Web Scraper)
Standard WordPress permalinks:
- ✅ `https://blog.com/2024/01/15/post-title/` (date-based)
- ❌ `https://blog.com/post-title/` (post name only)
- ❌ `https://blog.com/?p=123` (default/numeric)

**For non-standard URLs, use Method 1 (XML Export) instead.**

### File Encoding
- All files saved as **UTF-8**
- Handles international characters (emoji, accents, etc.)
- Compatible with all modern text editors

### Performance
- **XML Parser:** ~50-100 posts/second
- **Web Scraper:** ~1 post/second (due to polite 1-second delay)

---

## Scripts Included

### 1. `wordpress_xml_parser_with_dates.py` ⭐ RECOMMENDED
- Parses WordPress XML exports
- Includes dates in filenames
- Creates master CSV index
- Handles large files and CDATA sections
- Sorts posts chronologically

### 2. `wordpress_scraper.py`
- Web scraping alternative
- No WordPress login needed
- Best for recent posts only

### 3. `xml_analyzer.py`
- Diagnostic tool
- Shows XML structure
- Helps troubleshoot parsing issues

### 4. `diagnostic.py`
- Analyzes web scraping results
- Shows which URLs are found/rejected
- Helps understand URL filtering

### 5. `make_printfriendly_pdfs_v2.py` (Optional)
- Generates visual PDF versions of blog posts
- Preserves images and formatting
- Creates print-ready archive
- Complements text extraction
- Requires blog to be online

---

## Example Use Cases

### 1. Complete Blog Backup
```bash
# Export all posts from WordPress
# Run XML parser
python wordpress_xml_parser_with_dates.py myblog.xml
# Result: All 825 posts backed up with dates

# Optional: Generate PDF versions
python make_printfriendly_pdfs_v2.py
# Result: Visual PDF archive with images
```

### 2. Migrate to Another Platform
```bash
# Extract all posts
# Use the CSV index to map old URLs to new
# Import text files to new platform
```

### 3. Create a Searchable Archive
```bash
# Extract all posts
# Use Windows search or grep to find content
# Open specific posts by date or title
```

### 4. Analyze Writing Over Time
```bash
# Posts are sorted chronologically
# Open CSV in Excel
# Create charts showing posting frequency over time
```

---

## Frequently Asked Questions

### How many posts can this handle?
Tested successfully with 825 posts. Should handle thousands without issue.

### Does it download images?
No, only text content. Images remain on the blog.

### Can I re-run the script?
Yes, it will overwrite existing files with the same names.

### What about comments on posts?
Comments are removed. Only the post content is extracted.

### Does it work with custom WordPress themes?
Yes for XML export. Web scraper works best with standard themes.

### Can I use this on other people's blogs?
- XML export: Only if you have WordPress admin access
- Web scraper: Works on any public blog, but be respectful

### What if my blog uses a different platform?
This is designed specifically for WordPress. Other platforms have different export formats.

---

## Version History

**v2.0 (Current)** - Enhanced XML Parser
- ✅ Dates in filenames
- ✅ Chronological sorting
- ✅ Master CSV index
- ✅ Handles CDATA sections
- ✅ Robust error handling

**v1.0** - Initial Release
- Basic XML parser
- Web scraper
- Simple text extraction

---

## Support & Troubleshooting

### Common Error Messages

**"not well-formed (invalid token)"**
- XML file is corrupted
- Use the robust parser: `wordpress_xml_parser_with_dates.py`

**"No published posts found"**
- Make sure you exported Posts (not Pages)
- Check that posts are Published (not Draft)

**"Could not find content div"**
- Normal warning, posts still extracted
- Occurs with older/different themes

### Getting Help

If scripts don't work:
1. Run the diagnostic tools (`xml_analyzer.py` or `diagnostic.py`)
2. Check that Python and libraries are installed correctly
3. Verify your XML export or blog URL is correct
4. Make sure you're using the recommended XML parser method

---

## Best Practices

### ✅ DO:
- Use XML export method for complete archives
- Keep the CSV index for easy reference
- Back up the XML file itself
- Test with a few posts first on large blogs

### ❌ DON'T:
- Delete the XML export file (keep as backup)
- Modify the script without understanding it
- Run web scraper too frequently (respect server load)
- Expect images to be included (text only)

---

## License

Free to use and modify for personal projects.

---

## Quick Start Checklist

- [ ] Install Python 3.x
- [ ] Install required libraries (`pip install requests beautifulsoup4 lxml`)
- [ ] Export blog from WordPress (Tools → Export → Posts)
- [ ] Download `wordpress_xml_parser_with_dates.py`
- [ ] Run: `python wordpress_xml_parser_with_dates.py yourfile.xml`
- [ ] Open `exported_posts` folder to see results
- [ ] Open `_INDEX_ALL_POSTS.csv` in Excel

**That's it! You now have all your blog posts backed up as clean text files.**

---

**Created:** November 2025  
**Tested with:** WordPress.com, 825 posts, 9 years of content  
**Works with:** Windows, Mac, Linux
