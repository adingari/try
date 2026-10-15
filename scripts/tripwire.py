#!/usr/bin/env python3
"""Block commits that contain personal strings from a local tripwire list.

The list lives outside the repo (default ~/.try/tripwire.txt, override with
TRY_TRIPWIRE) so the list itself can never leak. One term per line,
case-insensitive, lines starting with # are comments. It fails closed: a
missing or empty list blocks the commit.

Modes:
  (no args)     staged changes: added lines and file names
  --msg FILE    a commit message file
  --tree        every tracked file, as staged
  --history     every commit on every branch, messages included
"""
import os
import subprocess
import sys

LIST = os.path.expanduser(os.environ.get("TRY_TRIPWIRE", "~/.try/tripwire.txt"))


def load_terms():
    try:
        with open(LIST, encoding="utf-8") as f:
            terms = [t.strip().lower() for t in f if t.strip() and not t.startswith("#")]
    except FileNotFoundError:
        sys.exit("tripwire: no list at %s. Create it (one term per line) first." % LIST)
    if not terms:
        sys.exit("tripwire: %s is empty." % LIST)
    return terms


def git(*args):
    out = subprocess.run(["git"] + list(args), capture_output=True, check=True).stdout
    return out.decode("utf-8", errors="replace")


def scan(label, text, terms):
    """One message per hit. Names the term and the place, never the line itself."""
    hits = []
    for n, line in enumerate(text.splitlines(), 1):
        low = line.lower()
        hits += ["%s, line %d: tripwire term '%s'" % (label, n, t) for t in terms if t in low]
    return hits


def staged(terms):
    hits = scan("staged file names", git("diff", "--cached", "--name-only"), terms)
    diff = git("diff", "--cached", "-U0", "--no-color")
    added = "\n".join(l[1:] for l in diff.splitlines() if l.startswith("+") and not l.startswith("+++"))
    return hits + scan("staged changes", added, terms)


def tree(terms):
    hits = []
    for path in git("ls-files", "-z").split("\0"):
        if not path:
            continue
        hits += scan("file name " + path, path, terms)
        hits += scan(path, git("show", ":" + path), terms)
    return hits


def history(terms):
    try:
        text = git("log", "--all", "-p", "--format=%B")
    except subprocess.CalledProcessError:
        return []  # no commits yet
    return scan("history", text, terms)


def main(argv):
    terms = load_terms()
    if argv[:1] == ["--msg"]:
        with open(argv[1], encoding="utf-8", errors="replace") as f:
            hits = scan("commit message", f.read(), terms)
    elif argv[:1] == ["--tree"]:
        hits = tree(terms)
    elif argv[:1] == ["--history"]:
        hits = history(terms)
    else:
        hits = staged(terms)
    for h in dict.fromkeys(hits):
        print("tripwire: " + h, file=sys.stderr)
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
