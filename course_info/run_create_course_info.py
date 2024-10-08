import os
import re
from scrape_course_catalogs import scrape_course_catalog, create_course_catalog_files

def create_course_folders(catalog_file, department_code, base_dir):
    # Ensure the base directory exists
    os.makedirs(base_dir, exist_ok=True)

    # Regular expression pattern to match course entries
    course_pattern = re.compile(
        rf'{department_code}\s+(\d{{3,4}})\.?\s+([^\.]+)\.?\s+\d+\s+Credits\.\s+(.*?)(?=\n\n|\Z)',
        re.DOTALL | re.MULTILINE
    )

    # Read the content of the course catalog
    with open(catalog_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # Find all courses in the catalog
    courses = course_pattern.findall(content)

    # Create department-level README.md
    dept_readme_path = os.path.join(base_dir, 'README.md')
    catalog_file_path = os.path.join(base_dir, 'course_catalog.txt')
    
    with open(catalog_file_path, 'r', encoding='utf-8') as catalog_file:
        catalog_content = catalog_file.read()
    
    # Convert the content to markdown
    markdown_content = f"# {department_code} Course Catalog\n\n"
    
    # Regular expression to match course entries
    course_pattern = re.compile(r'(\w+\s+\d+)\.\s+(.*?)\.\s+(\d+)\s+Credits\.\s+(.*?)(?=\n\n|\Z)', re.DOTALL)
    
    matches = course_pattern.findall(catalog_content)
    for match in matches:
        course_code, course_name, credits, description = match
        markdown_content += f"## {course_code}. {course_name}. {credits} Credits.\n\n"
        markdown_content += f"{description.strip()}\n\n"
    
    with open(dept_readme_path, 'w', encoding='utf-8') as dept_readme_file:
        dept_readme_file.write(markdown_content)

    print(f"Created department-level README.md for {department_code}")

    for course in courses:
        course_number = course[0].strip()
        course_name = course[1].strip()
        course_description = course[2].strip().replace('\n', ' ')
        
        # Clean the course name for folder naming
        course_name_clean = re.sub(r'[^\w\s-]', '', course_name).replace(' ', '_')
        
        # Folder name format: DEPT_101_Course_Name
        folder_name = f"{department_code}_{course_number}_{course_name_clean}"
        folder_path = os.path.join(base_dir, folder_name)

        # Create the course folder
        os.makedirs(folder_path, exist_ok=True)

        # Create and write to README.md
        readme_path = os.path.join(folder_path, 'README.md')
        with open(readme_path, 'w', encoding='utf-8') as readme_file:
            readme_content = f"# {department_code} {course_number}: {course_name}\n\n{course_description}"
            readme_file.write(readme_content)

        print(f"Created folder and README for {department_code} {course_number}")

def read_department_codes(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def run_create_course_info():
    # Read department codes from the text file
    department_codes_file = 'department_codes.txt'
    department_codes = read_department_codes(department_codes_file)

    # Step 1: Create or update course_catalog.txt files
    print("Step 1: Creating/updating course_catalog.txt files")
    #create_course_catalog_files(department_codes)

    # Step 2: Create individual course folders and README files
    print("\nStep 2: Creating individual course folders and README files")
    for dept in department_codes:
        catalog_file = os.path.join(dept, 'course_catalog.txt')
        if os.path.exists(catalog_file):
            print(f"Processing {dept}...")
            create_course_folders(catalog_file, dept, dept)
        else:
            print(f"Skipping {dept}: course_catalog.txt not found")

if __name__ == "__main__":
    run_create_course_info()