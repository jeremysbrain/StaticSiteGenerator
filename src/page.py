import block

import os
import subprocess
import shutil

def extract_title(markdown):
    # Extract the title from the markdown
    # The title is the first line of level 1 heading
    markdown_lines = markdown.split('\n')
    for line in markdown_lines:
        if line.startswith('# '):
            return line[2:].strip()
    return None

def generate_page(from_path, template_path, dest_path, basepath_dir):
    print(f"Generating HTML page from {from_path} to {dest_path} using template {template_path}")
    # Read the markdown file
    with open(from_path, 'r') as file:
        markdown = file.read()
        
    # Extract the title
    title = extract_title(markdown)
    if title is None:
        title = "Untitled Page"

    # Read the template file
    with open(template_path, 'r') as file:
        template = file.read()
    
    # Convert markdown to HTML node and then to HTML string
    html_node = block.markdown_to_html_node(markdown)
    html_content = html_node.to_html()
    
    # Replace the title and content in the template
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_content)

    # Add basepath directory
    template = template.replace("href=\"/", f"href=\"{basepath_dir}")
    template = template.replace("src=\"/", f"src=\"{basepath_dir}")

    # Write the generated HTML to the destination file
    with open(dest_path, 'w') as file:
        file.write(template)
        
    print(f"Generated HTML page saved to {dest_path}")

def generate_pages_recursively(content_dir, template_path, public_dir, basepath_dir):
    """
    Recursively generate HTML pages from markdown files while maintaining directory structure
    """
    # Create the public directory if it doesn't exist
    os.makedirs(public_dir, exist_ok=True)
    
    for item in os.listdir(content_dir):
        content_path = os.path.join(content_dir, item)
        public_path = os.path.join(public_dir, item)
        
        if os.path.isfile(content_path):
            if item.endswith('.md'):
                # Convert .md files to .html
                html_path = public_path.replace('.md', '.html')
                generate_page(content_path, template_path, html_path, basepath_dir)
        elif os.path.isdir(content_path):
            # Create corresponding directory in public and recurse
            generate_pages_recursively(content_path, template_path, public_path, basepath_dir)

def copy_static():
    directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go up one level from src
    static_dir = os.path.join(directory, 'static')
    public_dir = os.path.join(directory, 'docs')
    temp_zip = 'temp.zip'  # Just the filename, since we're changing directory
    original_dir = os.getcwd()  # Store original directory at the start
    
    try:
        # Check if static directory exists
        if not os.path.exists(static_dir):
            raise Exception(f"Static directory not found: {static_dir}")
        
        # Change to static directory for zip operation
        os.chdir(static_dir)
        
        # Zip from within static directory
        subprocess.run(['zip', '-r', '-v', os.path.join('..', temp_zip), '.'], check=True)
    
        # Change to project root for unzip
        os.chdir(directory)
        subprocess.run(['unzip', '-o', temp_zip, '-d', 'docs'], check=True)
        
        # Replace the ls commands with find
        static_files = set(subprocess.check_output(
            #['find', static_dir, '-type', 'f', '-printf', '%f\n']
            ['find', static_dir, '-type', 'f']
        ).decode('utf-8').splitlines())

        public_files = set(subprocess.check_output(
            #['find', public_dir, '-type', 'f', '-printf', '%f\n']
            ['find', public_dir, '-type', 'f']
        ).decode('utf-8').splitlines())

        # Check if each static file exists in public
        #missing_files = static_files - public_files
        #if missing_files:
        #    print(missing_files)
        #    raise Exception(f"Verification failed: Missing files in public: {missing_files}")
        #else:
        #    print("Verification successful: All files copied to public")
            
    finally:
        # Always try to return to original directory
        os.chdir(original_dir)
        # Clean up temp zip file if it exists
        if os.path.exists(os.path.join(directory, temp_zip)):
            os.remove(os.path.join(directory, temp_zip))