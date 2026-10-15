#!/usr/bin/env bash
# Run before the first push, and any time you doubt the repo. Read-only.
set -uo pipefail
cd "$(git rev-parse --show-toplevel)"
fail=0

email=$(git config user.email)
case "$email" in
  *@users.noreply.github.com) echo "ok   commit email is a GitHub noreply address" ;;
  *) echo "FAIL commit email is '$email', not a GitHub noreply address"; fail=1 ;;
esac

if git rev-parse HEAD >/dev/null 2>&1; then
  gitleaks git --redact . || fail=1          # every commit
else
  echo "ok   no commits yet, history scan skipped"
fi
gitleaks dir --redact . || fail=1            # working folder, tracked or not
python3 scripts/tripwire.py --tree || fail=1
python3 scripts/tripwire.py --history || fail=1

risky=$(git ls-files | grep -Ei '\.(png|jpe?g|gif|heic|pdf|stl|zip|env|pem|key|jsonl)$' || true)
if [ -n "$risky" ]; then
  echo "WARN these tracked files can carry metadata or private content. Review each:"
  echo "$risky"
  fail=1
fi

[ "$fail" -eq 0 ] && echo "PREFLIGHT PASSED" || echo "PREFLIGHT FAILED"
exit "$fail"
