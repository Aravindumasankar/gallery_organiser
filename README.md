# Gallery Organiser Starter Pack

This repository provides a minimal starting point for building a gallery
organiser application. It includes simple data models for artworks, a
command line interface for adding and listing pieces, and a React-based web
interface for browsing media files.

## Features

- Data models using Python dataclasses
- Command line interface for adding and listing artworks
- Web interface built with React for browsing media files
- Built-in file browser to navigate folders and preview images
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

4. **Launch the web UI**

   ```bash
   python -m gallery_organiser serve
   ```

   Then open <http://127.0.0.1:5000> in your browser and use the file
   browser to navigate folders and preview images.

Artworks are stored in `gallery_data.json` in the project root.

## License

This project is released under the MIT license.
