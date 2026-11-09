# Milestone 1 | AI-Powered Network Diagnostics and IT Risk Assessment Agent

Open `Milestone_1_Progress.pdf` for the submission write-up. The initial Skill is in `.agents/skills/diagnose-order-entry/SKILL.md`. The screenshots show the saved outputs from the recorded run. The corresponding plain-text logs and Codex's assessment are in `evidence/`.

## Reproduce the workflow on Linux

The evidence was collected by Codex in ChatGPT Work on remote Debian Linux with Python 3.12.14, Node.js 24.22.1, curl 8.14.1, and iproute2 ss 6.15.0. The lab uses Python and Node standard libraries. Run Codex and both fixtures in the same environment. The fixtures bind only to IPv4 loopback and require UDP port 15353 and TCP port 8765 to be free.

From the extracted project directory, run one command in each of two terminals:

```sh
python3 lab/fixture.py dns
python3 lab/fixture.py http
```

Once both fixtures print `READY`, use this prompt in a Codex session with access to the same directory and services:

> Read and use .agents/skills/diagnose-order-entry/SKILL.md. Check the lab health endpoint. Give the evidence, your verification, and the limits of your conclusion.

This is the explicit file-loading method used for the submitted run. If each command starts in a fresh execution environment, start the fixtures and run all probes within the same shell session. For the stopped-listener comparison, stop the HTTP fixture with Ctrl+C while leaving the DNS fixture running, repeat the same request, and then restart HTTP and retest. Stop both fixtures at the end.

The Skill uses `PROC_ROOT=/proc ss -4ltn` with an exact port filter. That invocation was verified against both listener states on the remote Linux environment. If socket inspection prints a permission error, treat the listener state as unverified until you can obtain a working local inspection result.
