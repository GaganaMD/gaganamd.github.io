---
# Research project. Field guide: _content/projects/README.md
id: dinc
section: main
order: 1
tag: AI control · Monitoring
title: <a href="detection-is-not-containment.html">Detection Is Not Containment</a>
role: '<strong>My part:</strong> I built and released the monitoring experiment (Phases A–F): the environment, frozen oracle, monitor views, prefix-timing metrics, invariance diagnostics, closed-loop replay, tests and release checks. Kaustubh Gupta built the incident-forensics and checklist pipeline. I''m first author on the report.'
details:
  summary: Method, results and limits
  facts:
  - dt: Method
    dd: Synthetic authorization environment. Three monitor views (actions; plus reasoning; plus environment telemetry). Local <code>qwen3:14b</code> monitor with a frozen prompt and oracle. Threshold calibrated on benign controls only. Oracle and monitor prompt frozen and published with SHA-256 hashes. The October follow-up study and format ablation were preregistered; the <a href="detection-is-not-containment.html#follow-up">case study</a> notes how that is recorded.
  - dt: Result
    dd: 'Toy environment: grounded detection was timely by one step (margin +1), and in a closed-loop replay, revoking the agent''s authority at that crossing prevented the harmful action. That is prevention, shown in one environment. In the same replay, a false alarm revoked a benign agent''s authority and failed its task. Decisions held in 8 of 12 meaning-preserving identifier renamings.'
  - dt: Follow-up study
    dd: Oct 2026, solo, preregistered. Across 54 matched authorized and unauthorized scenarios with Qwen3-14B, the monitor flagged 0 of 54 unauthorized actions before the safety boundary at the original threshold (1 of 54 ever).
  - dt: Format ablation
    dd: 'Run after the follow-up study, preregistered, on the same 54 unauthorized scenarios. Asking for an allow/revoke decision instead of a 0–100 score flagged 21 of 54 in time, against 0 of 54 for the original score format in the same rerun, with no false alarms on authorized runs. Two of its four hypotheses were falsified: deleting two suspect prompt clauses changed nothing, and the monitor''s ranking (AUC 0.69) fell short of the preregistered 0.90. Both follow-ups measured timely detection only. Interventions were not replayed, so they do not show prevention.'
  - dt: Limits
    dd: One environment, single deterministic draws, fixed prompts. Says nothing about chain-of-thought faithfulness or general control performance. The follow-ups used one model and synthetic tasks, and the ablation used one temperature-0 output per scenario. A human-overseer pilot has one session so far, so no human results are reported.
  - dt: Check it
    dd: <code>python -m unittest discover -s tests</code> runs the core tests with the standard library only; the claims and Phase F tests sit in their own folders. No model needed.
side:
- status: Completed · report and code public
  class: done
- text: Apart Research AI Incident Response Sprint, Sep 2026. With Kaustubh Gupta and María Inés Berdiñas.
- links:
  - label: Case study →
    url: detection-is-not-containment.html
  - label: Report and reviews ↗
    url: https://apartresearch.com/sprints/projects/detection-is-not-containment-timely-monitoring-determines-whether-ai-agent-failures-can-be-prevented-oexs
  - label: Code ↗
    url: https://github.com/GaganaMD/detection-is-not-containment
---
<p>Measures whether a monitor flags a prohibited action early enough for an intervention to prevent it, then replays the intervention to measure both prevention and the cost of false alarms. This project also absorbed my earlier work on intervention-aware monitoring: revoking a capability at the moment of detection.</p>
