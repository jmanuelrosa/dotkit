import hashlib
import importlib.util
import json
from importlib.machinery import SourceFileLoader
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
LOADER = SourceFileLoader("dotkit_vendor", str(ROOT / "bin" / "dotkit-vendor"))
vendor = importlib.util.module_from_spec(importlib.util.spec_from_loader(LOADER.name, LOADER))
LOADER.exec_module(vendor)

REV = "0123456789abcdef0123456789abcdef01234567"


@pytest.fixture
def consumer(tmp_path):
    (tmp_path / "pkg").mkdir()
    (tmp_path / "dotkit.json").write_text(json.dumps({"target": "pkg"}))
    return tmp_path


def lock(consumer):
    return json.loads((consumer / "dotkit.json").read_text())


def test_vendoring_copies_the_modules_and_records_what_it_copied(consumer):
    vendor.vendor(consumer, REV)
    recorded = lock(consumer)
    assert recorded["target"] == "pkg"
    assert recorded["rev"] == REV
    for name in vendor.MODULES:
        data = (consumer / "pkg" / name).read_bytes()
        assert data == (ROOT / "dotkit" / name).read_bytes()
        assert recorded["files"][name] == hashlib.sha256(data).hexdigest()


def test_a_fresh_copy_has_not_drifted(consumer):
    vendor.vendor(consumer, REV)
    assert vendor.check(consumer) == 0


def test_an_edited_copy_is_reported(consumer, capsys):
    vendor.vendor(consumer, REV)
    with (consumer / "pkg" / "ui.py").open("a") as copy:
        copy.write("# local edit\n")
    assert vendor.check(consumer) == 1
    assert "edited after vendoring" in capsys.readouterr().err


def test_a_copy_behind_dotkit_is_reported(consumer, capsys):
    vendor.vendor(consumer, REV)
    stale = lock(consumer)
    (consumer / "pkg" / "colors.py").write_text("old\n")
    stale["files"]["colors.py"] = hashlib.sha256(b"old\n").hexdigest()
    (consumer / "dotkit.json").write_text(json.dumps(stale))
    assert vendor.check(consumer) == 1
    assert "behind dotkit" in capsys.readouterr().out


def test_a_consumer_without_a_lock_is_refused(tmp_path):
    with pytest.raises(vendor.Refusal, match="no dotkit.json"):
        vendor.vendor(tmp_path, REV)


def test_a_lock_naming_a_missing_directory_is_refused(consumer):
    (consumer / "dotkit.json").write_text(json.dumps({"target": "absent"}))
    with pytest.raises(vendor.Refusal, match="not a directory"):
        vendor.check(consumer)
