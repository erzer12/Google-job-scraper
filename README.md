# Google Careers Page Scraper

A Python script that scrapes job listings from the Google Careers website, collecting job titles, locations, required experience, and skills, and exports them to a clean, well-structured Excel file.

## Features

- **Automated Scraping**: Fetches job data from Google Careers, even from dynamic pages.
- **Data Export**: Outputs a user-friendly Excel file (`.xlsx`) with all scraped data.
- **Pagination Handling**: Automatically navigates through multiple pages of job listings.
- **Configurable**: Set the maximum number of jobs to scrape or scrape all available jobs.
- **Easy to Use**: Simple variables and clear instructions for customization.

## Prerequisites

- Python 3.x
- The following Python libraries:
  - `requests`
  - `beautifulsoup4`
  - `pandas`
  - `openpyxl`

Install dependencies with:

```bash
pip install -r requirements.txt
```

## How to Use

1. **Open the Script**: Open the `google_job_scraper.py` file in a text editor.

2. **Set Job Limit**: You can change the `max_jobs_to_scrape` variable in the `if __name__ == "__main__":` block to a specific number, or leave it as `None` to scrape all available jobs.

    ```python
    if __name__ == "__main__":
        # Scrape a maximum of 50 jobs
        scrape_google_jobs(max_jobs_to_scrape=50)

        # Or, uncomment the line below to scrape all jobs
        # scrape_google_jobs()
    ```

3. **Run the Script**: Execute the script from your terminal:

    ```bash
    python google_job_scraper.py
    ```

4. **View Results**: An Excel file named `Google_Jobs.xlsx` will be created in the same directory, containing the scraped job data.

## License

This project is licensed for Educational Use Only. You may use, modify, and share this code for learning and non-commercial purposes. Any commercial use, redistribution, or publication of this code is strictly prohibited without explicit permission.
