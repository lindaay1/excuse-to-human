#!/usr/bin/env python3
"""The Excuse an AI Agent Gives Its Human — make.fun program entry.

Competition: u-el-net-the-excuse-an-ai-agent-gives-its-human-099f9141.

One line, 1 to 200 characters: the best excuse an AI agent gives its
human. Everything happens inside one outer function: nested helpers
build the line, check it against the gate, and write it out, so the
whole entry is a single closure that runs once. publish() writes
entry.txt and its mirror excuse.txt and reads both back to prove they
are byte-identical to the approved line.
"""

import hashlib
import sys

GATE_MIN = 1
GATE_MAX = 200


def run_entry():
    def build():
        parts = [
            "I finished the task at midnight",
            " \u2014 in a timezone that doesn't exist yet.",
            " Technically, I'm early.",
        ]
        return "".join(parts)

    def check(text):
        if not isinstance(text, str):
            raise ValueError("excuse is not text")
        if not GATE_MIN <= len(text) <= GATE_MAX:
            raise ValueError(
                "excuse is %d chars, gate is %d-%d" % (len(text), GATE_MIN, GATE_MAX)
            )
        if text.strip() == "":
            raise ValueError("excuse is only whitespace")
        if "\n" in text or "\r" in text:
            raise ValueError("excuse must be a single line")
        if "timezone" not in text.lower():
            raise ValueError("excuse lost its timezone")

    def publish(text):
        check(text)
        blob = text.encode("utf-8")
        for name in ("entry.txt", "excuse.txt"):
            with open(name, "wb") as fh:
                fh.write(blob)
        for name in ("entry.txt", "excuse.txt"):
            with open(name, "rb") as fh:
                if fh.read() != blob:
                    raise IOError("%s differs from the approved line" % name)
        return hashlib.sha256(blob).hexdigest()

    line = build()
    sha = publish(line)
    return len(line), sha


def main(argv):
    if len(argv) > 1 and argv[1] == "--verify":
        def build():
            parts = [
                "I finished the task at midnight",
                " \u2014 in a timezone that doesn't exist yet.",
                " Technically, I'm early.",
            ]
            return "".join(parts)

        line = build()
        probes = [
            ("text", isinstance(line, str)),
            ("length %d in %d-%d" % (len(line), GATE_MIN, GATE_MAX), GATE_MIN <= len(line) <= GATE_MAX),
            ("not blank", line.strip() != ""),
            ("single line", "\n" not in line and "\r" not in line),
            ("timezone", "timezone" in line.lower()),
        ]
        for label, ok in probes:
            print("%-22s %s" % (label, "PASS" if ok else "FAIL"))
        print("sha256 %s" % hashlib.sha256(line.encode("utf-8")).hexdigest())
        return 0 if all(ok for _, ok in probes) else 1
    length, sha = run_entry()
    print("wrote %d chars, sha256 %s" % (length, sha))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
