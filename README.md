# Gallery Organiser Starter Pack v2

This repository provides a minimal starting point for building a gallery
organiser application. It includes simple data models for artworks, a
command line interface for adding and listing pieces, and a React-based web
interface for browsing media files.

## Features

- Data models using Python dataclasses
- Command line interface for adding and listing artworks
- Web interface built with React for browsing media files
- Built-in file browser to navigate folders and preview images
- AI-powered image classification using a Hugging Face model
- Optional face detection with tagging and name-based search
- Scanning starts only when confirmed and shows a log console of activity
- Labels and face tags are stored in a SQLite database for later lookup
- Shows scanning progress and reports skipped items when directories are inaccessible
- Basic unit tests
- Optional Docker support for containerised deployment

The React frontend provides a modern two-panel layout. Select a folder,
click **Scan**, and thumbnails with predicted labels will appear. The log
console at the bottom records scanning activity. You can tag detected faces
and later search by person name.

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

   Then open <http://127.0.0.1:5000> in your browser. Use the built-in file
   browser to pick a directory, press **Scan**, and view a gallery-style grid
   of images with automatic labels. The log console records progress and any
   inaccessible files that were skipped. Use the **Tag** button on an image to
   associate a detected face with a name, then search for tagged people with
   the search box.

5. **Run with Docker**

   ```bash
   docker compose up --build
   ```

   This builds an image with all dependencies installed and serves the
   application on <http://127.0.0.1:5000>.

You can check the installed version with:

```bash
python -m gallery_organiser --version
```

Artworks are stored in `gallery_data.json` in the project root. Labels and
face tags are kept in `gallery.db`.

## License

This project is released under the MIT license.
