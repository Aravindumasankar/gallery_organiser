"""Tkinter-based GUI for browsing media files."""
from __future__ import annotations

from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

from PIL import Image, ImageTk
import pillow_heif

from .media import scan_media


class GalleryUI(tk.Tk):
    """Simple window that lets users browse media files."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Gallery Organiser")
        self.geometry("800x600")
        self._build_widgets()
        self.media_files: list[Path] = []
        self.preview_image: ImageTk.PhotoImage | None = None

    def _build_widgets(self) -> None:
        toolbar = tk.Frame(self)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        tk.Button(toolbar, text="Open Folder", command=self.open_folder).pack(side=tk.LEFT)

        self.listbox = tk.Listbox(self)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox.bind("<<ListboxSelect>>", self.show_preview)

        self.preview_label = tk.Label(self)
        self.preview_label.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def open_folder(self) -> None:
        path = filedialog.askdirectory()
        if path:
            self.media_files = scan_media(Path(path))
            self.listbox.delete(0, tk.END)
            for p in self.media_files:
                self.listbox.insert(tk.END, p.name)
            self.preview_label.configure(image="", text="")

    def show_preview(self, event: tk.Event[tk.Listbox]) -> None:  # pragma: no cover - GUI event
        if not self.listbox.curselection():
            return
        path = self.media_files[self.listbox.curselection()[0]]
        suffix = path.suffix.lower()
        if suffix in {".mp4", ".mov", ".mkv"}:
            self.preview_label.configure(text=path.name)
            return
        try:
            if suffix == ".heic":
                heif_file = pillow_heif.read_heif(str(path))
                image = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data, "raw")
            else:
                image = Image.open(path)
            image.thumbnail((400, 400))
            self.preview_image = ImageTk.PhotoImage(image)
            self.preview_label.configure(image=self.preview_image)
        except Exception as exc:  # pragma: no cover - UI feedback
            messagebox.showerror("Error", f"Could not load image: {exc}")


def run_gui() -> None:
    """Launch the graphical gallery browser."""
    app = GalleryUI()
    app.mainloop()


if __name__ == "__main__":  # pragma: no cover
    run_gui()
