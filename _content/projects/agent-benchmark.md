---
# Research project. Field guide: _content/projects/README.md
id: agent-benchmark
section: main
order: 4
tag: Evaluation infrastructure · Industry
title: Benchmark for long-horizon finance agent tasks
role: <strong>My part:</strong> I designed and built the harness, grading engine and run pipeline at BaseThesis Labs (Bengaluru, May–Jul 2026).
details:
  summary: Details
  facts:
  - dt: Check it
    dd: 'The public release has 50 tests and two synthetic demo tasks: <code>python -m pytest -q</code>.'
  - dt: Status
    dd: Industry project, mid 2026. The public release is code only. Task banks, client documents and results stay private.
side:
- status: Code public · data private
  class: done
- links:
  - label: Code ↗
    url: https://github.com/GaganaMD/synth-benchmark-public
---
<p>An offline-first harness for evaluating agents on long-horizon and ultra-long-horizon CFO and financial due-diligence work over messy files. Task packages are generated from one canonical task file. Grading is rubric-based, with contradictions, unsafe actions and prompt-injection compliance as automatic failures. A leakage guard refuses to grade if answer files are visible to the agent.</p>
