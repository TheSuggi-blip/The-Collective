"""A circuit's hunt step with `alone: "pirates"` keeps that rule in hunt.py (it left for every stranger before)."""

from pathlib import Path
import re
import unittest

FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"


class StepAloneTests(unittest.TestCase):
    def test_route_run_passes_the_step_rule(self):
        text = (FLEET / "route_run.py").read_text(encoding="ascii")
        self.assertIn("command += ['--alone-mode', 'pirates'] if step.get('alone') == 'pirates' else []", text)

    def test_hunt_takes_the_step_rule(self):
        text = (FLEET / "hunt.py").read_text(encoding="ascii")
        self.assertTrue(re.search(r"if ALONE and STEP and '--alone-mode' in args and args\[args\.index\('--alone-mode'\) \+ 1\] == 'pirates':\n\s+ALONE_MODE = 'pirates'", text))


if __name__ == "__main__":
    unittest.main()
