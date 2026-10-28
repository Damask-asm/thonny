"""Run with the bundled Python, outside the source directory."""
import ast
import json
import os
import queue
import subprocess
import sys
import tempfile
import threading
from pathlib import Path


def main():
    import thonny
    from thonny.common import (
        DebuggerCommand, DebuggerResponse, InlineCommand, ToplevelCommand,
        ToplevelResponse, parse_message, serialize_message,
    )

    package = Path(thonny.__file__).parent
    assert package.is_relative_to(Path(sys.executable).parent), package
    source = (package / "workbench.py").read_text(encoding="utf-8")
    ast.parse(source)
    ast.parse((package / "__init__.py").read_text(encoding="utf-8"))
    assert all(x not in source for x in ["SupportUkraine", "Support Ukraine", "_support_ukraine", 'image="Ukraine"'])
    assert (package / "locale" / "ru_RU" / "LC_MESSAGES" / "thonny.mo").exists()
    assert Path(thonny.THONNY_USER_DIR).name == "Thonny-Classroom", thonny.THONNY_USER_DIR

    with tempfile.TemporaryDirectory(prefix="classroom-test-") as temp:
        env = os.environ.copy()
        env["THONNY_USER_DIR"] = str(Path(temp) / "profile")
        script = Path(temp) / "lesson.py"
        script.write_text("a = 20\nb = 22\nanswer = a + b\nprint('CLASSROOM_RESULT', answer)\n")
        proc = subprocess.Popen(
            [sys.executable, "-u", "-B", str(package / "plugins/cpython_backend/cp_launcher.py"), temp, "{}"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, encoding="utf-8", env=env, cwd=temp,
        )
        messages = queue.Queue()

        def read():
            for line in proc.stdout:
                messages.put(line)
            messages.put(None)

        threading.Thread(target=read, daemon=True).start()

        def send(msg):
            proc.stdin.write(serialize_message(msg) + "\n")
            proc.stdin.flush()

        def receive():
            while True:
                line = messages.get(timeout=40)
                assert line is not None, "Backend exited"
                if line.startswith("\x02"):
                    return parse_message(line)

        def complete():
            output = ""
            while True:
                msg = receive()
                assert not msg.get("error"), repr(msg)
                output += msg.get("data", "")
                if isinstance(msg, ToplevelResponse):
                    assert not msg.get("user_exception"), repr(msg)
                    return output

        try:
            send(ToplevelCommand("get_environment_info"))
            complete()
            send(ToplevelCommand("Run", args=[str(script)], breakpoints={}))
            assert "CLASSROOM_RESULT 42" in complete()
            send(InlineCommand("get_globals", module_name="__main__"))
            msg = receive()
            assert msg.globals["answer"].repr == "42", repr(msg)
            send(ToplevelCommand("Debug", args=[str(script)], breakpoints={}))
            steps, output, observed_answer = 0, "", False
            while True:
                msg = receive()
                assert not msg.get("error"), repr(msg)
                output += msg.get("data", "")
                if isinstance(msg, DebuggerResponse):
                    steps += 1
                    assert msg.stack
                    frame = msg.stack[-1]
                    values = frame.locals or frame.globals or {}
                    if "answer" in values:
                        observed_answer |= values["answer"].repr == "42"
                    assert steps < 200
                    send(DebuggerCommand("step_into", frame_id=frame.id, state=frame.event,
                                         focus=frame.focus, breakpoints={}, exception=None))
                elif isinstance(msg, ToplevelResponse):
                    assert not msg.get("user_exception"), repr(msg)
                    break
            assert steps > 2 and observed_answer and "CLASSROOM_RESULT 42" in output, (steps, observed_answer, output)
            print(json.dumps({"bundled_python": sys.version, "package": str(package),
                              "execution": "42", "globals": "42", "debug_steps": steps,
                              "debug_variables": "42", "source_ui_check": "passed"}))
        finally:
            proc.kill()
            proc.communicate(timeout=10)


if __name__ == "__main__":
    main()
