# google_job_scraper.py
# This script scrapes job listings from the Google Careers page,
# extracts key information, and saves it to an Excel file.

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

def scrape_google_jobs(max_jobs_to_scrape=None):
    """
    Main function to orchestrate the scraping process.
    It iterates through pages, scrapes job data, and saves it to an Excel file.

    Args:
        max_jobs_to_scrape (int, optional): The maximum number of jobs to scrape. 
                                            If None, all available jobs will be scraped.
    """
    # Base URL for Google Careers
    # Note: This is kept for constructing the initial URL and for potential future use.
    base_url = "https://www.google.com/about/careers/applications/"
    
    # Starting URL for the job listings
    initial_url = base_url + "jobs/results"

    # List to store all scraped job data
    all_jobs = []
    
    # The URL to scrape, starting with the initial page
    current_url = initial_url
    
    # Counter for the number of pages scraped
    page_count = 1

    # Loop to handle pagination
    while current_url:
        # Check if we have scraped enough jobs
        if max_jobs_to_scrape and len(all_jobs) >= max_jobs_to_scrape:
            print(f"Reached the requested number of jobs ({max_jobs_to_scrape}). Stopping scrape.")
            break

        print(f"Scraping page {page_count}: {current_url}")
        
        try:
            # Send an HTTP GET request to the current URL
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
            }
            response = requests.get(current_url, headers=headers)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all job listings. The main container is a <ul> with class 'spHGqe'.
            # Each job listing is an <li> with class 'lLd3Je'.
            job_listings = soup.find_all('li', class_='lLd3Je')

            if not job_listings:
                print("No more job listings found. Ending scrape.")
                break

            # Process each job listing
            for listing in job_listings:
                # Check if we have scraped enough jobs before adding the new one
                if max_jobs_to_scrape and len(all_jobs) >= max_jobs_to_scrape:
                    break

                job_data = {}

                # 1. Extract JobTitle
                try:
                    job_data['JobTitle'] = listing.find('h3', class_='QJPWVe').text.strip()
                except AttributeError:
                    job_data['JobTitle'] = "N/A"

                # 2. Extract Location
                try:
                    locations = [loc.text.strip() for loc in listing.find_all('span', class_='r0wTof')]
                    # Use a set to get unique locations before joining
                    job_data['Location'] = ', '.join(sorted(list(set(locations))))
                except AttributeError:
                    job_data['Location'] = "N/A"

                # 3. Extract ExperienceRequired
                try:
                    experience_span = listing.find('span', class_='wVSTAb')
                    if experience_span:
                        job_data['ExperienceRequired'] = experience_span.text.strip()
                    else:
                        job_data['ExperienceRequired'] = "Not Specified"
                except AttributeError:
                    job_data['ExperienceRequired'] = "N/A"
                
                # 4. Extract SkillsRequired
                # The minimum qualifications are a good proxy for skills.
                try:
                    skills_list = []
                    # Find the header for minimum qualifications
                    qualifications_h4 = listing.find('h4', string=lambda s: s and 'Minimum qualifications' in s)
                    if qualifications_h4:
                        # Find the immediately following <ul> which contains the list items
                        skills_ul = qualifications_h4.find_next_sibling('ul')
                        if skills_ul:
                            # Extract text from each list item
                            skills_list = [li.text.strip() for li in skills_ul.find_all('li')]
                            job_data['SkillsRequired'] = ' '.join(skills_list)
                        else:
                            job_data['SkillsRequired'] = "Not Specified"
                    else:
                        job_data['SkillsRequired'] = "Not Specified"
                except (AttributeError, TypeError):
                    job_data['SkillsRequired'] = "N/A"

                # 5. Extract Salary (often not available, so handle gracefully)
                # The Google Careers site does not list salary information publicly on the search page,
                # so we will leave this field blank as requested.
                job_data['Salary'] = ""
                
                # 6. Extract JobURL
                try:
                    # Find the 'Learn more' link and extract its href attribute
                    job_url_tag = listing.find('a', class_='WpHeLc')
                    if job_url_tag:
                        # The href attribute is a full URL, so use it directly
                        job_data['JobURL'] = job_url_tag['href']
                    else:
                        job_data['JobURL'] = "N/A"
                except (AttributeError, TypeError):
                    job_data['JobURL'] = "N/A"
                
                # 7. Extract JobDescriptionSummary
                # Similar to skills, use the qualifications as a summary.
                job_data['JobDescriptionSummary'] = job_data['SkillsRequired']
                
                all_jobs.append(job_data)

            # Find the next page link to continue the loop
            next_page_tag = soup.find('a', {'aria-label': 'Go to next page'})
            if next_page_tag and 'href' in next_page_tag.attrs:
                # The href is a full URL, so assign it directly
                current_url = next_page_tag['href']
                page_count += 1
                # Add a delay to avoid overwhelming the server
                time.sleep(2)
            else:
                # If there's no next page button, stop the loop
                current_url = None
                
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            break

    # Convert the list of dictionaries to a pandas DataFrame
    df = pd.DataFrame(all_jobs)

    # If the scraped jobs exceed the requested number, trim the DataFrame
    if max_jobs_to_scrape and len(df) > max_jobs_to_scrape:
        df = df.iloc[:max_jobs_to_scrape]

    # Clean the DataFrame before saving
    if 'Salary' in df.columns:
        df['Salary'] = df['Salary'].replace("N/A", "")

    # Define the output file name as per the project description
    output_filename = "Google_Jobs.xlsx"
    
    # Export the DataFrame to an Excel file
    try:
        df.to_excel(output_filename, index=False)
        print(f"\nSuccessfully scraped {len(df)} jobs and saved to '{output_filename}'")
    except Exception as e:
        print(f"Failed to save data to Excel file: {e}")

# This ensures the function is called only when the script is executed directly
if __name__ == "__main__":
    # Example: Scrape a maximum of 50 jobs
    scrape_google_jobs(max_jobs_to_scrape=50)

    # To scrape all jobs, you can call the function without an argument
    # scrape_google_jobs()
