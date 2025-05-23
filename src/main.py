from textnode import *

import page
import os
import shutil
import sys

def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go up one level from src
    static_dir = os.path.join(directory, 'static')
    public_dir = os.path.join(directory, 'docs')
    
    # Remove the public directory if it exists
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir, ignore_errors=True)
    # Create the public directory
    os.makedirs(public_dir) 
   
    # Copy the static files to the public directory
    page.copy_static()

    # Generate the index page
    page.generate_pages_recursively(os.path.join(directory, 'content'), os.path.join(directory, 'template.html'), public_dir, basepath)

if __name__ == "__main__":
    main()