import os
import re

def get_user_input():
    catalog_file = input("Enter the name of the course catalog file (e.g., courses_catalog.txt): ")
    department_code = input("Enter the department code (e.g., COMP): ")
    base_dir = input("Enter the base directory name for the course folders (e.g., COMP): ")
    return catalog_file, department_code, base_dir

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

    for course in courses:
        course_number = course[0].strip()
        course_name = course[1].strip()
        course_description = course[2].strip().replace('\n', ' ')
        
        # Clean the course name for folder naming
        course_name_clean = re.sub(r'[^\w\s-]', '', course_name).replace(' ', '_')
        
        # Folder name format: DEPT_101_Course_Name
        folder_name = f"{department_code}_{course_number}_{course_name_clean}"
        folder_path = os.path.join(base_dir, folder_name)

        print(folder_path)
        
        # Create the course folder
        os.makedirs(folder_path, exist_ok=True)

        # Create and write to README.md
        readme_path = os.path.join(folder_path, 'README.md')
        with open(readme_path, 'w', encoding='utf-8') as readme_file:
            readme_content = f"# {department_code} {course_number}: {course_name}\n\n{course_description}"
            readme_file.write(readme_content)

        print(f"Created folder and README for {department_code} {course_number}")

def create_catalog_readme(catalog_file, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Read the content of the course catalog
    with open(catalog_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # Extract department code from the first course entry
    first_course_match = re.search(r'([A-Z]+)\s+\d{3,4}\.?\s+', content)
    if first_course_match:
        department_code = first_course_match.group(1)
    else:
        department_code = "UNKNOWN"

    # Create README content
    readme_content = f"# {department_code} Course Catalog\n\n"
    
    # Regular expression to match course entries
    course_pattern = re.compile(
        rf'({department_code}\s+\d{{3,4}})\.?\s+([^\.]+)\.?\s+\d+\s+Credits\.\s+(.*?)(?=\n\n|\Z)',
        re.DOTALL | re.MULTILINE
    )

    # Find all courses in the catalog
    courses = course_pattern.findall(content)

    for course in courses:
        course_code = course[0].strip()
        course_name = course[1].strip()
        course_description = course[2].strip().replace('\n', ' ')
        
        readme_content += f"## {course_code}: {course_name}\n\n{course_description}\n\n"

    # Write README.md
    readme_path = os.path.join(output_folder, 'README.md')
    with open(readme_path, 'w', encoding='utf-8') as readme_file:
        readme_file.write(readme_content)

    print(f"Created README.md for {department_code} course catalog in {output_folder}")

def main():
    action = input("Choose an action (1: Create course folders, 2: Create catalog README): ")
    
    if action == '1':
        catalog_file, department_code, base_dir = get_user_input()
        create_course_folders(catalog_file, department_code, base_dir)
        print("Course folders and README files have been created successfully.")
    elif action == '2':
        catalog_file = input("Enter the name of the course catalog file: ")
        output_folder = input("Enter the output folder for README.md: ")
        create_catalog_readme(catalog_file, output_folder)
    else:
        print("Invalid action. Please choose 1 or 2.")

if __name__ == "__main__":
    main()