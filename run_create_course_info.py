import os
import re

def create_course_folders(catalog_file, department_code, base_dir):
    # Ensure the base directory exists
    os.makedirs(base_dir, exist_ok=True)

    # Read the content of the course catalog
    with open(catalog_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # Regular expression pattern to match course entries
    course_pattern = re.compile(
        rf'({department_code}\s+\d{{3,4}}.*?)\n(.*?)(?=\n\n|\Z)',
        re.DOTALL | re.MULTILINE
    )

    # Find all courses in the catalog
    courses = course_pattern.findall(content)

    # Create department-level README.md
    dept_readme_path = os.path.join(base_dir, 'README.md')
    with open(dept_readme_path, 'w', encoding='utf-8') as dept_readme_file:
        dept_readme_content = f"# {department_code} Course Catalog\n\n"
        for course_title, course_description in courses:
            course_number = course_title.split()[1]
            course_name = ' '.join(course_title.split()[2:])
            folder_name = f"{department_code}_{course_number}_{course_name.replace(' ', '_')}"
            dept_readme_content += f"## [{course_title}]({folder_name})\n\n{course_description}\n\n"
        dept_readme_file.write(dept_readme_content)

    print(f"Created department-level README.md for {department_code}")

    for course_title, course_description in courses:
        course_number = course_title.split()[1]
        course_name = ' '.join(course_title.split()[2:])
        
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
            readme_content = f"# {course_title}\n\n{course_description}"
            readme_file.write(readme_content)

        print(f"Created folder and README for {department_code} {course_number}")