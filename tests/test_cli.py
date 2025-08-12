import sys
from pathlib import Path

# Ensure package root on path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from gallery_organiser import cli, gui


def test_gui_command_invokes_run_gui(monkeypatch):
    called = {}

    def fake_run_gui():
        called['ran'] = True

    monkeypatch.setattr(gui, 'run_gui', fake_run_gui)
    cli.main(['gui'])
    assert called.get('ran') is True
