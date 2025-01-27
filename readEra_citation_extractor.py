'''
ReadEra Citation Extractor
---
This script allows you to extract all citations from all books opened in ReadEra.\n
Select the latest Backup (.bak) File from your Android here: Internal Storage / ReadEra / BackUps\n
It will save the citations from each book in a separate txt

version
---
1.0.0
'''

import json
import tkinter.filedialog
import zipfile
import os

def extract_citations(library, output_dir):
    try:
        # Open and read the JSON file
        with open(library, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Iterate through documents in the JSON data
        for doc in data.get('docs', []):
            # Get the document title or assign a default value
            book_title = doc.get('data', {}).get('doc_file_name_title', 'unknown_title')
            citations = doc.get('citations', [])
            
            # If citations are available, write them to a text file in the same folder as .bak
            output_file_path = os.path.join(output_dir, f'{book_title}.txt')
            if citations:
                with open(output_file_path, 'w', encoding='utf-8') as output_file:
                    for citation in citations:
                        citation_text = citation.get('note_body', 'No citation text')
                        page_number = citation.get('note_page', 'Unknown page')
                        output_file.write(f'Page {page_number}: {citation_text}\n')
                print(f'Extracted citations for: {book_title}, saved to {output_file_path}')
            else:
                print(f'No citations found for: {book_title}')
    
    except Exception as e:
        print(f"Error processing library file: {e}")

def extract_library():
    try:
        # Prompt user to select a .bak file
        bak_file = tkinter.filedialog.askopenfilename(
            filetypes=[("Backup Files", "*.bak")], 
            defaultextension=".bak",
            title="Select .bak file"
        )
        
        if not bak_file:
            print("No file selected. Exiting.")
            return None, None

        # Extract the .bak file assuming it is a zip archive
        extract_dir = os.path.dirname(bak_file)
        with zipfile.ZipFile(bak_file, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
            print(f"Extracted contents to: {extract_dir}")
            
            # Look for the expected JSON file in extracted contents
            library_path = os.path.join(extract_dir, "library.json")
            if os.path.exists(library_path):
                return library_path, extract_dir
            else:
                print("library.json not found in extracted files.")
                return None, None

    except zipfile.BadZipFile:
        print("Selected file is not a valid .zip format.")
        return None, None
    except Exception as e:
        print(f"Error extracting .bak file: {e}")
        return None, None

if __name__ == "__main__":
    library, output_dir = extract_library()
    if library:
        extract_citations(library, output_dir)
    else:
        print("Failed to extract library data.")