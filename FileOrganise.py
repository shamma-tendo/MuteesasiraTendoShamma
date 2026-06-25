#!/usr/bin/env python3
"""
File Organizer Script for Downloads Folder
Organizes files into subfolders based on file extensions and categories
"""

import os
import shutil
import datetime
import argparse
from pathlib import Path
import sys
import fnmatch

# File category definitions
FILE_CATEGORIES = {
    'images': {
        'extensions': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg', '.ico', '.raw'],
        'folder_name': 'Images'
    },
    'documents': {
        'extensions': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.pages', '.tex', '.wpd'],
        'folder_name': 'Documents'
    },
    'spreadsheets': {
        'extensions': ['.xls', '.xlsx', '.csv', '.ods', '.numbers'],
        'folder_name': 'Spreadsheets'
    },
    'presentations': {
        'extensions': ['.ppt', '.pptx', '.odp', '.key'],
        'folder_name': 'Presentations'
    },
    'archives': {
        'extensions': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.tgz', '.z', '.jar', '.war'],
        'folder_name': 'Archives'
    },
    'audio': {
        'extensions': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a', '.aiff', '.alac'],
        'folder_name': 'Audio'
    },
    'video': {
        'extensions': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.mpg', '.mpeg'],
        'folder_name': 'Video'
    },
    'code': {
        'extensions': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.go', '.rs', '.php', 
                      '.rb', '.swift', '.kt', '.ts', '.jsx', '.tsx', '.vue', '.sql', '.sh', '.bash'],
        'folder_name': 'Code'
    },
    'executables': {
        'extensions': ['.exe', '.msi', '.app', '.deb', '.rpm', '.dmg', '.pkg', '.sh', '.bat', '.cmd'],
        'folder_name': 'Executables'
    },
    'fonts': {
        'extensions': ['.ttf', '.otf', '.woff', '.woff2', '.eot', '.fon'],
        'folder_name': 'Fonts'
    },
    'ebooks': {
        'extensions': ['.epub', '.mobi', '.azw', '.azw3', '.fb2', '.lit'],
        'folder_name': 'Ebooks'
    },
    '3d_models': {
        'extensions': ['.stl', '.obj', '.fbx', '.blend', '.3ds', '.dae', '.glb', '.gltf'],
        'folder_name': '3D Models'
    },
    'backup': {
        'extensions': ['.bak', '.old', '.tmp', '.temp', '.swp', '.sav'],
        'folder_name': 'Backup'
    }
}

# Custom user-defined rules (format: {'extension': 'folder_name'})
CUSTOM_RULES = {
    # Example: '.log': 'Logs'
}

class FileOrganizer:
    def __init__(self, download_path=None, create_category_folders=True, 
                 move_files=True, dry_run=False, organize_by_date=False,
                 date_folder_format='%Y-%m'):
        """
        Initialize the File Organizer
        
        Args:
            download_path: Path to the downloads folder (default: user's Downloads)
            create_category_folders: Whether to create category folders
            move_files: Whether to move files (if False, copies them)
            dry_run: If True, only simulates operations without making changes
            organize_by_date: If True, organizes files by date within category folders
            date_folder_format: Format for date subfolders (if organize_by_date is True)
        """
        if download_path is None:
            self.download_path = Path.home() / 'Downloads'
        else:
            self.download_path = Path(download_path)
            
        self.create_category_folders = create_category_folders
        self.move_files = move_files
        self.dry_run = dry_run
        self.organize_by_date = organize_by_date
        self.date_folder_format = date_folder_format
        self.stats = {
            'processed': 0,
            'moved': 0,
            'copied': 0,
            'skipped': 0,
            'errors': 0,
            'error_details': []
        }
        
        # Merge custom rules with categories
        self.categories = FILE_CATEGORIES.copy()
        self._add_custom_rules()
        
    def _add_custom_rules(self):
        """Add custom rules to the categories"""
        for ext, folder_name in CUSTOM_RULES.items():
            # Add extension to an existing category or create new one
            category_found = False
            for category in self.categories.values():
                if category['folder_name'] == folder_name:
                    category['extensions'].append(ext.lower())
                    category_found = True
                    break
            
            if not category_found:
                # Create new category
                self.categories[f'custom_{folder_name}'] = {
                    'extensions': [ext.lower()],
                    'folder_name': folder_name
                }
    
    def _get_file_category(self, filename):
        """Determine the category of a file based on its extension"""
        file_extension = Path(filename).suffix.lower()
        
        # Check custom rules first
        for category, info in self.categories.items():
            if file_extension in info['extensions']:
                return info['folder_name']
        
        # If no match, return 'Other'
        return 'Other'
    
    def _get_relative_date_path(self, file_path):
        """Get date-based subfolder path for a file"""
        try:
            # Get file modification time
            mtime = os.path.getmtime(file_path)
            date_obj = datetime.datetime.fromtimestamp(mtime)
            return date_obj.strftime(self.date_folder_format)
        except Exception:
            # If we can't get the date, use current date
            return datetime.datetime.now().strftime(self.date_folder_format)
    
    def _safe_move(self, source, destination):
        """Safely move a file, handling duplicates"""
        if destination.exists():
            # Handle duplicate file
            base_name = destination.stem
            extension = destination.suffix
            counter = 1
            
            while True:
                new_name = f"{base_name}_{counter}{extension}"
                new_dest = destination.parent / new_name
                if not new_dest.exists():
                    destination = new_dest
                    break
                counter += 1
        
        try:
            if self.dry_run:
                print(f"[DRY RUN] Would {'move' if self.move_files else 'copy'} '{source}' to '{destination}'")
                return True
            
            if self.move_files:
                shutil.move(str(source), str(destination))
                self.stats['moved'] += 1
            else:
                shutil.copy2(str(source), str(destination))
                self.stats['copied'] += 1
            return True
            
        except Exception as e:
            error_msg = f"Error processing '{source}': {str(e)}"
            print(error_msg, file=sys.stderr)
            self.stats['errors'] += 1
            self.stats['error_details'].append(error_msg)
            return False
    
    def organize(self):
        """Main method to organize the downloads folder"""
        print(f" Organizing files in: {self.download_path}")
        print(f" Mode: {'DRY RUN (no changes)' if self.dry_run else 'LIVE'}")
        print(f" Action: {'Move' if self.move_files else 'Copy'} files")
        print(f" Date organization: {'Enabled' if self.organize_by_date else 'Disabled'}")
        print("-" * 50)
        
        # Check if downloads folder exists
        if not self.download_path.exists():
            print(f" Error: Downloads folder '{self.download_path}' does not exist.")
            return False
        
        # Get list of all files in downloads folder
        files_to_process = []
        for item in self.download_path.iterdir():
            if item.is_file():
                # Skip hidden files (starting with .)
                if item.name.startswith('.'):
                    continue
                files_to_process.append(item)
        
        if not files_to_process:
            print(" No files to organize!")
            return True
        
        print(f" Found {len(files_to_process)} files to process")
        
        # Create category folders and organize files
        for file_path in files_to_process:
            file_name = file_path.name
            category = self._get_file_category(file_name)
            
            # Determine target folder
            target_folder = self.download_path / category
            
            # Add date subfolder if enabled
            if self.organize_by_date:
                date_subfolder = self._get_relative_date_path(file_path)
                target_folder = target_folder / date_subfolder
            
            # Create target folder if it doesn't exist
            if self.create_category_folders and not target_folder.exists():
                if self.dry_run:
                    print(f"[DRY RUN] Would create folder: {target_folder}")
                else:
                    try:
                        target_folder.mkdir(parents=True, exist_ok=True)
                    except Exception as e:
                        print(f" Error creating folder '{target_folder}': {e}", file=sys.stderr)
                        self.stats['errors'] += 1
                        continue
            
            # Skip if file is already in the correct location
            if file_path.parent == target_folder:
                print(f" Skipping '{file_name}' - already in correct location")
                self.stats['skipped'] += 1
                continue
            
            # Move/copy file to target folder
            destination = target_folder / file_name
            if self._safe_move(file_path, destination):
                self.stats['processed'] += 1
                
                # Print progress
                action = "Moved" if self.move_files else "Copied"
                print(f"✓ {action}: '{file_name}' → {category}")
        
        # Print statistics
        self._print_statistics()
        return True
    
    def _print_statistics(self):
        """Print organization statistics"""
        print("\n" + "=" * 50)
        print(" ORGANIZATION SUMMARY")
        print("=" * 50)
        print(f" Total files processed: {self.stats['processed']}")
        print(f" Files moved: {self.stats['moved']}")
        print(f" Files copied: {self.stats['copied']}")
        print(f"  Files skipped: {self.stats['skipped']}")
        print(f" Errors encountered: {self.stats['errors']}")
        
        if self.stats['error_details']:
            print("\n Error details:")
            for error in self.stats['error_details']:
                print(f"  - {error}")
        
        if self.dry_run:
            print("\n This was a DRY RUN - no changes were made to your files.")
            print("   Remove the --dry-run flag to perform actual organization.")
        
        print("=" * 50)

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Organize files in your Downloads folder')
    parser.add_argument('-p', '--path', 
                       help='Path to downloads folder (default: user Downloads)',
                       default=None)
    parser.add_argument('--dry-run', 
                       action='store_true',
                       help='Simulate organization without making changes')
    parser.add_argument('--copy', 
                       action='store_true',
                       help='Copy files instead of moving them')
    parser.add_argument('--no-create', 
                       action='store_true',
                       help='Do not create category folders')
    parser.add_argument('--by-date', 
                       action='store_true',
                       help='Organize files by date within category folders')
    parser.add_argument('--date-format', 
                       default='%Y-%m',
                       help='Date format for subfolders (default: %%Y-%%m)')
    parser.add_argument('--custom-rules',
                       nargs='+',
                       help='Custom rules in format ext:folder (e.g., .log:Logs .tmp:Temp)')
    return parser.parse_args()

def setup_custom_rules(rules):
    """Setup custom rules from command line arguments"""
    if rules:
        for rule in rules:
            try:
                ext, folder = rule.split(':')
                CUSTOM_RULES[ext.lower()] = folder
                print(f"✓ Added custom rule: '{ext}' → '{folder}'")
            except ValueError:
                print(f" Invalid custom rule format: '{rule}'. Expected 'ext:folder'")

def main():
    """Main entry point"""
    args = parse_arguments()
    
    # Setup custom rules if provided
    if args.custom_rules:
        setup_custom_rules(args.custom_rules)
    
    # Create organizer instance
    organizer = FileOrganizer(
        download_path=args.path,
        create_category_folders=not args.no_create,
        move_files=not args.copy,
        dry_run=args.dry_run,
        organize_by_date=args.by_date,
        date_folder_format=args.date_format
    )
    
    # Run organization
    organizer.organize()

if __name__ == "__main__":
    main()