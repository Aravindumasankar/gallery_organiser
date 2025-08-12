import sys
from pathlib import Path

# Ensure package root on path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from gallery_organiser import cli, server


def test_serve_command_invokes_run_server(monkeypatch):
    called = {}

    def fake_run_server():
        called['ran'] = True

    monkeypatch.setattr(server, 'run_server', fake_run_server)
    cli.main(['serve'])
    assert called.get('ran') is True
