from gallery_organiser.server import app
from PIL import Image


def test_api_dirs(tmp_path):
    (tmp_path / "sub").mkdir()
    client = app.test_client()
    resp = client.get("/api/dirs", query_string={"path": str(tmp_path)})
    assert resp.status_code == 200
    assert str(tmp_path / "sub") in resp.get_json()


def test_api_file(tmp_path):
    img_path = tmp_path / "pic.png"
    Image.new("RGB", (1, 1)).save(img_path)
    client = app.test_client()
    resp = client.get("/api/file", query_string={"path": str(img_path)})
    assert resp.status_code == 200
    assert resp.mimetype == "image/png"
