# AsuraScans Downloader

A simple Python script that downloads every chapter of a manhwa from **AsuraScans** and converts each chapter into a **PDF**.

## Installation

Clone the repository:

```bash
git clone https://github.com/rawriie/asurascans-downloader.git
cd asurascans-downloader
```

Install the required packages:

```bash
pip install requests beautifulsoup4 pillow
```

## Usage

Run the script and provide the URL of the series page.

```bash
python main.py -u "https://asurascans.com/series/your-series"
```

## Notes

* This project is intended for educational and personal use.
* It currently supports **AsuraScans** only.
* The script depends on the current website structure. If AsuraScans changes its HTML layout, the scraper may stop working until updated.

## Disclaimer

Please respect the website's Terms of Service and the copyright of the content you access. Use this project only where you have permission to download or archive the material.
