#!/usr/bin/env python3
"""
Translation helper script for Construbot documentation .po files.

This script uses deep-translator (free Google Translate API) to translate
empty msgstr entries in .po files from English to Spanish.

Usage:
    python translate_po_files.py                    # Translate all .po files
    python translate_po_files.py file1.po file2.po  # Translate specific files
    python translate_po_files.py --dry-run          # Preview without changes

Requirements:
    pip install deep-translator polib
"""

import argparse
import os
import sys
import time
from pathlib import Path

try:
    from deep_translator import GoogleTranslator
    import polib
except ImportError:
    print("Error: Required packages not installed.")
    print("Please run: pip install deep-translator polib")
    sys.exit(1)


class POTranslator:
    def __init__(self, dry_run=False, verbose=False):
        self.translator = GoogleTranslator(source='en', target='es')
        self.dry_run = dry_run
        self.verbose = verbose
        self.stats = {
            'files_processed': 0,
            'entries_translated': 0,
            'entries_skipped': 0,
            'errors': 0
        }

    def translate_text(self, text):
        """Translate text with error handling and rate limiting."""
        if not text or not text.strip():
            return text

        try:
            # Rate limiting to avoid API throttling
            time.sleep(0.1)

            # Translate in chunks if text is too long (Google Translate limit ~5000 chars)
            if len(text) > 4500:
                # Split by sentences and translate in batches
                sentences = text.split('. ')
                translated_parts = []
                for sentence in sentences:
                    if sentence:
                        translated = self.translator.translate(sentence)
                        translated_parts.append(translated)
                return '. '.join(translated_parts)
            else:
                return self.translator.translate(text)

        except Exception as e:
            if self.verbose:
                print(f"    Warning: Translation error: {e}")
            self.stats['errors'] += 1
            return text  # Return original if translation fails

    def should_translate_entry(self, entry):
        """Determine if a PO entry should be translated."""
        # Skip if already translated
        if entry.msgstr and entry.msgstr.strip():
            return False

        # Skip if msgid is empty
        if not entry.msgid or not entry.msgid.strip():
            return False

        # Skip technical references like :ref:`genindex`
        if entry.msgid.startswith(':ref:') or entry.msgid.startswith(':doc:'):
            return False

        # Skip URLs
        if entry.msgid.startswith('http://') or entry.msgid.startswith('https://'):
            return False

        return True

    def translate_po_file(self, po_file_path):
        """Translate a single .po file."""
        po_file_path = Path(po_file_path)

        if not po_file_path.exists():
            print(f"Error: File not found: {po_file_path}")
            return False

        print(f"\nProcessing: {po_file_path}")

        try:
            po = polib.pofile(str(po_file_path))
        except Exception as e:
            print(f"Error: Failed to parse PO file: {e}")
            return False

        translated_count = 0
        skipped_count = 0

        for entry in po:
            if self.should_translate_entry(entry):
                if self.verbose:
                    print(f"  Translating: {entry.msgid[:60]}...")

                translated = self.translate_text(entry.msgid)

                if self.dry_run:
                    print(f"    [DRY RUN] Would translate to: {translated[:60]}...")
                else:
                    entry.msgstr = translated

                translated_count += 1
            else:
                skipped_count += 1

        if not self.dry_run and translated_count > 0:
            po.save()
            print(f"  ✓ Translated {translated_count} entries, skipped {skipped_count}")
        elif self.dry_run:
            print(f"  [DRY RUN] Would translate {translated_count} entries, skip {skipped_count}")
        else:
            print(f"  No entries to translate (skipped {skipped_count})")

        self.stats['files_processed'] += 1
        self.stats['entries_translated'] += translated_count
        self.stats['entries_skipped'] += skipped_count

        return True

    def translate_directory(self, directory):
        """Recursively translate all .po files in a directory."""
        directory = Path(directory)

        if not directory.exists():
            print(f"Error: Directory not found: {directory}")
            return False

        po_files = list(directory.rglob('*.po'))

        if not po_files:
            print(f"No .po files found in {directory}")
            return False

        print(f"Found {len(po_files)} .po files")

        for po_file in po_files:
            self.translate_po_file(po_file)

        return True

    def print_summary(self):
        """Print translation statistics."""
        print("\n" + "="*60)
        print("Translation Summary")
        print("="*60)
        print(f"Files processed:     {self.stats['files_processed']}")
        print(f"Entries translated:  {self.stats['entries_translated']}")
        print(f"Entries skipped:     {self.stats['entries_skipped']}")
        print(f"Errors:              {self.stats['errors']}")
        print("="*60)


def main():
    parser = argparse.ArgumentParser(
        description='Translate Construbot documentation .po files from English to Spanish'
    )
    parser.add_argument(
        'files',
        nargs='*',
        help='Specific .po files to translate (default: all in locale/es/LC_MESSAGES/)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview translations without modifying files'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show detailed progress'
    )
    parser.add_argument(
        '--dir',
        default='locale/es/LC_MESSAGES',
        help='Directory containing .po files (default: locale/es/LC_MESSAGES)'
    )

    args = parser.parse_args()

    translator = POTranslator(dry_run=args.dry_run, verbose=args.verbose)

    if args.files:
        # Translate specific files
        for file_path in args.files:
            translator.translate_po_file(file_path)
    else:
        # Translate all files in directory
        translator.translate_directory(args.dir)

    translator.print_summary()


if __name__ == '__main__':
    main()
