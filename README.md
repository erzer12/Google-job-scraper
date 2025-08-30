# Internshala Job Scraper

This Python script automates the process of scraping job listings from Internshala.com, extracting key details, and saving the data into a structured Excel file. It is a simple and efficient tool for collecting job-related information.

## Features

- **Data Scraping**: Extracts job titles, locations, experience levels, skills, salaries, and job descriptions from the Internshala jobs page.
- **Detailed Insights**: Retrieves additional details by following links to individual job pages.
- **Excel Export**: Saves all scraped data into a well-organized `Jobs.xlsx` file.
- **Readable Output**: Automatically adjusts column widths in the Excel file for better readability.

## Prerequisites

- Python 3.6 or higher.
- Required Python libraries installed.

## Installation

1. Clone the repository or save the Python script and `requirements.txt` in the same directory.
2. Install the required libraries using pip:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the scraper by executing the Python script in your terminal:

```bash
python scraper.py
```

The script will scrape job data and generate a file named `Jobs.xlsx` in the same directory.

> **Note**: The script includes a small delay (`time.sleep(0.5)`) between requests to ensure responsible scraping practices and avoid overwhelming the server.
