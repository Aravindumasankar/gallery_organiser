# Gallery Organiser Starter Pack

This repository provides a minimal starting point for building a gallery
organiser application. It includes simple data models for artworks and a
command line interface for adding and listing pieces in a gallery.

## Features

- Data models using Python dataclasses
- Command line interface for adding and listing artworks
- Graphical interface for browsing media files
- Basic unit tests

## Getting Started

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run tests**

   ```bash
   pytest
   ```

3. **Use the CLI**

   ```bash
   python -m gallery_organiser add --title "Starry Night" --artist "Vincent van Gogh" --year 1889
   python -m gallery_organiser list
   ```
4. **Launch the GUI**

   ```bash
   python -m gallery_organiser gui
   ```

   Select a directory from the attached hard disk to browse images and videos. HEIC images are supported.

Artworks are stored in `gallery_data.json` in the project root.

## License

This project is released under the GNU General Public License v3.0 or later.
