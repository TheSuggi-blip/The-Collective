"""The station's chat session with an agent's door: fixtures only, no door and no network."""

import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
import urllib.error


SCRIPT = Path(__file__).resolve().parents[2] / "station" / "server.py"


class Answer:
    def __init__(self, value):
        self.value = value

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def read(self, n=-1):
        return json.dumps(self.value).encode("utf-8")


class StationChatTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location("station_under_test", SCRIPT)
        assert spec is not None and spec.loader is not None
        self.station = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.station)
        self.temp = tempfile.TemporaryDirectory(prefix="station-test-")
        self.addCleanup(self.temp.cleanup)
        self.station.DATA = Path(self.temp.name)
        self.agent = next(iter(self.station.CHATS))
        self.titles = []

    def door(self, taken=()):
        def hermes(agent, method, path, body=None, stream=False, timeout=60):
            self.titles.append(body["title"])
            if body["title"] in taken:
                raise urllib.error.HTTPError("http://door" + path, 400, "Bad Request", {}, io.BytesIO(b'{"error": "invalid_title", "message": "title in use"}'))
            return Answer({"session": {"id": "api_%d" % len(self.titles)}})
        self.station.hermes = hermes

    def test_a_session_is_made_once_and_kept(self):
        self.door()
        self.assertIsNone(self.station.chat_session(self.agent))
        self.assertEqual(self.station.chat_session(self.agent, create=True), "api_1")
        self.assertEqual(self.station.chat_session(self.agent, create=True), "api_1")
        self.assertEqual(self.titles, ["Command station"])
        self.assertEqual(json.loads((self.station.DATA / "chat.json").read_text())[self.agent], "api_1")

    def test_a_title_the_door_refuses_is_asked_again_with_a_title_of_its_own_time(self):
        # 2026-11-16: Zero's door answered 400 to the fixed title, an older session held it (queue.log ENT-118)
        self.door(taken=("Command station",))
        self.assertEqual(self.station.chat_session(self.agent, create=True), "api_2")
        self.assertEqual(self.titles[0], "Command station")
        self.assertRegex(self.titles[1], r"^Command station \(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d\)$")

    def test_another_refusal_is_not_hidden_and_the_error_line_says_what_the_door_answered(self):
        def hermes(agent, method, path, body=None, stream=False, timeout=60):
            raise urllib.error.HTTPError("http://door" + path, 401, "Unauthorized", {}, io.BytesIO(b'{"error": "bad key"}'))
        self.station.hermes = hermes
        with self.assertRaises(urllib.error.HTTPError) as caught:
            self.station.chat_session(self.agent, create=True)
        self.assertEqual(self.station.door_said(caught.exception), 'HTTPError 401 {"error": "bad key"}')
        self.assertEqual(self.station.door_said(TimeoutError("timed out")), "TimeoutError")


if __name__ == "__main__":
    unittest.main()
