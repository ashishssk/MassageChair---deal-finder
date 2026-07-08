# 🛠️ Step-by-Step Setup Guide for Massage Chair Deal Finder

## Prerequisites
Before you start, make sure you have:
- **Python 3.7 or higher** installed on your computer
- **Git** installed (to clone the repository)
- A text editor (like VSCode, Notepad++, or even Notepad)

---

## Step 1: Download the Repository to Your Computer

### Option A: Using Git (Recommended for Developers)
```bash
# Open Command Prompt or Terminal and run:
git clone https://github.com/ashishssk/MassageChair---deal-finder.git

# Navigate into the folder
cd MassageChair---deal-finder
```

### Option B: Download as ZIP (Easy for Beginners)
1. Go to: https://github.com/ashishssk/MassageChair---deal-finder
2. Click the green **"Code"** button
3. Click **"Download ZIP"**
4. Extract the ZIP file to a folder on your computer
5. Open that folder

---

## Step 2: Install Required Libraries

The script needs two special libraries to work. Open **Command Prompt** (Windows) or **Terminal** (Mac/Linux) in your project folder and run:

```bash
pip install requests beautifulsoup4
```

**What this does:**
- `requests` - downloads web pages
- `beautifulsoup4` - reads and finds data in those web pages

**How to verify installation:**
```bash
pip list
```
You should see both `requests` and `beautifulsoup4` in the list.

---

## Step 3: Update the Store URLs

Open the file **`price_finder.py`** in a text editor and find this section (around line 145):

```python
def main():
    """Main execution"""
    tracker = PriceTracker()
    
    # Example URLs - Replace with actual collection page URLs
    osaki_url = "https://www.osakiusa.com/collections/massage-chairs"
    ota_world_url = "https://www.otaworld.com/collections/massage-chairs"
    shopify_url = "https://your-shopify-store.myshopify.com/collections/massage-chairs"
```

### How to Find the Right URLs:

#### For OsakiUSA:
1. Go to https://www.osakiusa.com
2. Look for "Massage Chairs" or similar collection
3. Find the URL in the address bar (example: `https://www.osakiusa.com/collections/massage-chairs`)
4. Copy and paste it into the script

#### For OTAworld:
1. Go to https://www.otaworld.com (or their website)
2. Navigate to their massage chair collection
3. Copy the collection URL

#### For Shopify Stores:
1. Find the Shopify store you want to monitor
2. Navigate to their massage chair collection page
3. The URL typically looks like: `https://store-name.myshopify.com/collections/massage-chairs`

### Example of Updated URLs:
```python
osaki_url = "https://www.osakiusa.com/collections/massage-chairs-4d"
ota_world_url = "https://www.otaworld.com/collections/premium-massage-chairs"
shopify_url = "https://example-store.myshopify.com/collections/4d-massage-chairs"
```

---

## Step 4: Run the Script

Open **Command Prompt** (Windows) or **Terminal** (Mac/Linux) in your project folder:

```bash
python price_finder.py
```

**You should see:**
- 🔍 Scraping messages for each store
- ✅ Number of products found
- 💰 A list of products sorted by price
- 🎯 CHEAPEST DEAL label on the lowest price
- 🔥 BIG DISCOUNT label on discounts over 40%

---

## Step 5: View the Results

The script creates two output files:

### 📊 price_comparison.json
- Contains all data in JSON format
- Open with any text editor
- **Good for:** Developers, data analysis

### 📈 price_comparison.csv
- Contains all data in spreadsheet format
- Open with Excel or Google Sheets
- **Good for:** Easy viewing, sorting, filtering

---

## Troubleshooting Guide

### ❌ Error: "Python is not recognized"
**Solution:** Python is not installed or not added to PATH
- Download Python from https://www.python.org/downloads/
- During installation, **CHECK THE BOX** that says "Add Python to PATH"
- Restart Command Prompt and try again

### ❌ Error: "No module named 'requests'"
**Solution:** Libraries not installed
```bash
pip install requests beautifulsoup4
```

### ❌ Error: "Connection refused" or "Invalid URL"
**Solution:** The store URL might be wrong
- Double-check the URL in the script
- Make sure the URL leads to a collection/listing page (not a single product)
- Try visiting the URL in your browser first

### ❌ Script runs but finds 0 products
**Solution:** The website structure might be different
- The script uses common CSS selectors
- Some sites use different selectors
- You might need to inspect the website's HTML structure

**How to check (for advanced users):**
1. Open the store URL in a browser
2. Right-click on a product → "Inspect" or "Inspect Element"
3. Look for the class names used for products
4. Update the script with the correct selectors

### ❌ Error: "name 'datetime' is not defined"
**Solution:** Make sure you're using Python 3.7+
```bash
python --version
```

---

## Advanced: Automating the Script

### Run the Script Every Day (Windows)

1. Open **Task Scheduler**
2. Click **"Create Basic Task"**
3. Name it: "Massage Chair Deal Finder"
4. Choose frequency: "Daily"
5. Set the time (e.g., 9:00 AM)
6. Action: Start a program
   - Program: `python.exe`
   - Arguments: `price_finder.py`
   - Start in: Your project folder path

### Run the Script Every Day (Mac/Linux)

Add to crontab (runs at 9 AM daily):
```bash
0 9 * * * cd /path/to/script && python price_finder.py
```

---

## Tips for Best Results

✅ **Use specific collection URLs** - Don't use homepage URLs  
✅ **Update URLs periodically** - Store URLs can change  
✅ **Run regularly** - Check prices daily or weekly  
✅ **Export data** - Keep CSV files for historical comparison  
✅ **Check for 4D/3D** - Script filters for these features automatically  

---

## Need Help?

1. **Check the error message** - It usually tells you what's wrong
2. **Visit Python docs** - https://www.python.org/
3. **Install VSCode** - Makes debugging easier
4. **Run with verbose mode** - Add print statements to see what's happening

---

## Quick Reference Commands

```bash
# Check Python version
python --version

# Install libraries
pip install requests beautifulsoup4

# Run the script
python price_finder.py

# View installed libraries
pip list

# Upgrade pip
pip install --upgrade pip
```

---

**Happy deal hunting! 🎉**
