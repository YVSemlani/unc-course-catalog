import os
import requests
from bs4 import BeautifulSoup
import re

def scrape_course_catalog(department_code):
    url = f"https://catalog.unc.edu/courses/{department_code.lower()}/"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to fetch data for {department_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    course_blocks = soup.find_all('div', class_='courseblock')

    if not course_blocks:
        print(f"No course blocks found for {department_code}")
        return None

    catalog_content = ""
    for i, course in enumerate(course_blocks):
        # Extract course code
        code_elem = course.find('span', class_='text detail-code margin--tiny text--semibold text--big')
        if code_elem and code_elem.find('strong'):
            code = code_elem.find('strong').text.strip()
            # Remove the period at the end if it exists
            #code = code[:-1] if code.endswith('.') else code
        else:
            print(f"Course {i+1}: Unable to find course code")
            code = "Unknown_Code"

        # Extract course title
        title_elem = course.find('span', class_='text detail-title margin--tiny text--semibold text--big')
        if title_elem and title_elem.find('strong'):
            title = title_elem.find('strong').text.strip()
            # Remove the period at the end if it exists
            title = title[:-1] if title.endswith('.') else title
        else:
            print(f"Course {i+1}: Unable to find course title")
            title = "Unknown_Title"

        # Extract course credits
        credits_elem = course.find('span', class_='text detail-hours margin--tiny text--semibold text--big')
        if credits_elem and credits_elem.find('strong'):
            credits = credits_elem.find('strong').text.strip()
            # Remove the period at the end if it exists
            credits = credits[:-1] if credits.endswith('.') else credits
        else:
            print(f"Course {i+1}: Unable to find course credits")
            credits = "Unknown_Credits"

        # Combine code, title, and credits
        full_title = f"{code} {title}. {credits}."

        # Extract course description
        description = course.find('p', class_='courseblockextra')
        if description:
            description = description.text.strip()
            # Remove multiple spaces and newlines
            description = re.sub(r'\s+', ' ', description)
        else:
            print(f"Course {i+1}: Unable to find course description")
            description = "No description available."

        # Clean up the full title
        full_title = re.sub(r'\s+', ' ', full_title)

        # Append to catalog content
        catalog_content += f"{full_title}\n{description}\n\n"

    return catalog_content

def create_course_catalog_files(department_codes):
    # Iterate over each department code
    for dept in department_codes:
        print(f"Scraping catalog for {dept}...")
        catalog_content = scrape_course_catalog(dept)
        
        if catalog_content:
            # Define the path for course_catalog.txt
            catalog_path = os.path.join(dept, 'course_catalog.txt')
            
            # Write the catalog content to the file
            with open(catalog_path, 'w', encoding='utf-8') as f:
                f.write(catalog_content)
            print(f"Created course_catalog.txt for {dept}")
        else:
            print(f"No data found for {dept}\n")

def main():
    # Read department codes from the file
    with open('department_codes.txt', 'r') as file:
        department_codes = [line.strip() for line in file if line.strip()]
    
    print(f"Loaded {len(department_codes)} department codes.")
    create_course_catalog_files(department_codes)
    print("Scraping completed.")

if __name__ == "__main__":
    main()