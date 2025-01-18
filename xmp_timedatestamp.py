from pathlib import Path
import xml.etree.ElementTree as ET
import re

def prepend_date_to_filename(file_path, metadata_dir=None, whatif=False):
    """
    Takes a file and prepends its filename with the DateCreated attribute
    extracted from its XMP metadata, sanitizing unsafe characters. Optionally,
    searches for the relevant XMP metadata file in a specified directory.

    Args:
        file_path (str or Path): Path to the file.
        metadata_dir (str or Path, optional): Directory to search for the matching XMP metadata file.
        whatif (bool, optional): If True, reports what changes would be made without making them.

    Returns:
        Path: The new file path with the prepended DateCreated attribute.
    """
    try:
        file_path = Path(file_path)
        metadata_dir = Path(metadata_dir) if metadata_dir else None

        # Determine the XMP metadata file path
        if metadata_dir:
            filename_without_ext = file_path.stem
            xmp_file_path = metadata_dir / f"{filename_without_ext}.xmp"
        else:
            xmp_file_path = file_path

        # Parse the XMP metadata
        if not xmp_file_path.exists():
            raise FileNotFoundError(f"XMP metadata file not found: {xmp_file_path}")

        with xmp_file_path.open('r', encoding='utf-8') as file:
            content = file.read()

        # Parse XML and find DateCreated
        root = ET.fromstring(content)
        namespace = {'photoshop': 'http://ns.adobe.com/photoshop/1.0/'}
        date_created = root.find('.//photoshop:DateCreated', namespace)

        if date_created is None or not date_created.text:
            raise ValueError("DateCreated attribute not found in the XMP metadata.")

        # Extract and sanitize the date string
        sanitized_date = re.sub(r'[^A-Za-z0-9_-]', '_', date_created.text)

        # Prepend the sanitized date to the filename
        new_filename = f"{sanitized_date}_{file_path.name}"
        new_file_path = file_path.parent / new_filename

        if whatif:
            print(f"[WHATIF] Would rename '{file_path}' to '{new_file_path}'")
        else:
            # Rename the file
            file_path.rename(new_file_path)

        return new_file_path

    except Exception as e:
        raise RuntimeError(f"Error processing file '{file_path}': {e}")

# Example usage:
# file_path = "/path/to/your/image.jpg"
# metadata_dir = "/path/to/your/metadata"
# new_file_path = prepend_date_to_filename(file_path, metadata_dir=metadata_dir, whatif=True)
# print(f"File renamed to: {new_file_path}")

file_path = "/Users/davidmidlo/Library/Mobile Documents/iCloud~md~obsidian/Documents/iOS-Vault/Desk/AvarTec Records/Clients/Dorglass/Other/25-01-03/IMG_2293.png"
metadata_dir = "/Users/davidmidlo/Library/Mobile Documents/iCloud~md~obsidian/Documents/iOS-Vault/Desk/Unsorted Screenshots and Video/Raw and Metadata Files"
new_file_path = prepend_date_to_filename(file_path, metadata_dir=metadata_dir, whatif=False)
print(f"File renamed to: {new_file_path}")
