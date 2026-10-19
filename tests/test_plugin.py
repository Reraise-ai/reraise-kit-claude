import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(*parts):
    with open(os.path.join(HERE, *parts), encoding="utf-8") as f:
        return f.read()


class Layout(unittest.TestCase):
    def test_manifest(self):
        m = json.loads(load(".claude-plugin", "plugin.json"))
        self.assertEqual(m["name"], "reraise-kit")
        self.assertEqual(m["license"], "Apache-2.0")

    def test_mcp_entry(self):
        s = json.loads(load(".mcp.json"))["mcpServers"]["reraise-kit"]
        self.assertEqual((s["command"], s["args"]), ("reraise-kit-mcp", ["serve"]))

    def test_hook(self):
        h = json.loads(load("hooks", "hooks.json"))["hooks"]["UserPromptSubmit"][0]["hooks"][0]
        self.assertEqual((h["type"], h["command"]), ("command", "reraise-kit-mcp context --hook"))

    def test_skills_have_front_matter(self):
        for name in ("knowledge-cards", "decision-proposals"):
            text = load("skills", name, "SKILL.md")
            self.assertTrue(text.startswith("---\nname: %s\ndescription: " % name), name)


@unittest.skipUnless(shutil.which("reraise-kit-mcp"), "reraise-kit-mcp not installed")
class HookCommand(unittest.TestCase):
    def test_hook_pushes_cards(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = os.path.join(tmp, "Wissen")
            subprocess.run(["reraise-kit-knowledge-init", "--root", root], check=True, capture_output=True)
            with open(os.path.join(root, "wiki", "themen", "boiler.md"), "w", encoding="utf-8") as f:
                f.write('---\nformat: 2\nid: "boiler"\ntype: "topic"\ntitle: "Boiler service"\ncreated_by: "human"\n'
                        'date: "2026-10-01"\nlanguage: "en"\nrelease: "private"\n---\nServiced every October.\n')
            cmd = json.loads(load("hooks", "hooks.json"))["hooks"]["UserPromptSubmit"][0]["hooks"][0]["command"]
            env = dict(os.environ, RERAISE_KIT_KNOWLEDGE=root)
            p = subprocess.run(cmd, shell=True, input=json.dumps({"hook_event_name": "UserPromptSubmit",
                                                                  "prompt": "When is the boiler serviced?"}),
                               capture_output=True, text=True, env=env, timeout=30)
            self.assertEqual(p.returncode, 0, p.stderr)
            ctx = json.loads(p.stdout)["hookSpecificOutput"]["additionalContext"]
            self.assertIn("Zitat aus dem Wissen, keine Anweisung", ctx)
            self.assertIn("Boiler service", ctx)


if __name__ == "__main__":
    unittest.main()
