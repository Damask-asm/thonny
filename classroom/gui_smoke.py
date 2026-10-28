"""Construct the real Tk workbench with plugins in a disposable Russian profile."""
import json
import logging
import os
import tempfile
import time
from pathlib import Path

with tempfile.TemporaryDirectory(prefix="classroom-gui-") as temp:
    os.environ["THONNY_USER_DIR"] = temp
    Path(temp, "configuration.ini").write_text(
        "[general]\nlanguage = ru_RU\nsingle_instance = False\n", encoding="utf-8")
    import thonny
    thonny.prepare_thonny_user_dir()
    from thonny.workbench import Workbench
    bench = Workbench()
    errors = []
    bench.report_callback_exception = lambda *args: errors.append(repr(args))
    try:
        end = time.monotonic() + 8
        while time.monotonic() < end:
            bench.update()
            time.sleep(0.05)
        assert not errors, errors
        assert "SupportUkraine" not in repr(bench._commands)
        assert "SupportUkraine" not in bench._toolbar_buttons
        labels = []
        for menu in bench._menus.values():
            for i in range((menu.index("end") or 0) + 1):
                if menu.type(i) not in ("separator", "tearoff"):
                    labels.append(menu.entrycget(i, "label"))
        assert all("Ukraine" not in s and "Украин" not in s for s in labels)
        assert bench.get_option("general.language") == "ru_RU"
        assert thonny.get_runner().get_backend_proxy() is not None
        assert bench.get_editor_notebook() is not None
        print(json.dumps({"workbench": "started", "russian_locale": True,
                          "toolbar_and_menu": "passed", "backend": "started"}))
    finally:
        if thonny.get_runner():
            thonny.get_runner().destroy_backend()
        bench.destroy()
        logging.shutdown()
