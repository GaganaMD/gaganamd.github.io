---
# Research project. Field guide: _content/projects/README.md
id: collusion
section: main
order: 2
tag: Multi-agent safety · Collusion
title: What can we infer about colluding agents from their behaviour?
role: <strong>My part:</strong> On the pricing project, I implemented the mechanistic interpretability and steering experiments (probes, activation patching, steering against random-direction controls). On the peer-swap project, I led the RepeatedJira experiment, in which a monitor covertly takes over a colluder's seat.
details:
  summary: Method, results and limits
  facts:
  - dt: Peer swaps
    dd: <a href="https://apartresearch.com/sprints/projects/noticing-the-move-missing-the-player-llm-agents-detect-behavioral-shifts-but-not-peer-swaps-uf7r">Noticing the Move, Missing the Player</a>. In a Diner's Dilemma, a Public Goods Game and a RepeatedJira collusion setup, agents tracked behaviour, not identity. In the Public Goods Game study (led by Kaustubh Gupta), 0 of 468 probes named a silent swap, while free riding was clearly detected (AUC 0.915–0.984). In the RepeatedJira study I led, a monitor that covertly took a colluder's seat ended the collusion in all 10 Qwen3 pairs, and the remaining agent never mentioned a replacement (0 of 15 episodes; results tables public, raw logs not yet released). With V S Siva Kumar Lakkoju and Kaustubh Gupta.
  - dt: Tacit pricing
    dd: <a href="https://apartresearch.com/sprints/projects/tacit-collusion-in-pricing-agents-robustness-detection-and-a-mechanistic-probe-of-a-pricing-llm-qxsb">Tacit Collusion in Pricing Agents</a>. One fixed, competitive agent broke a collusive pricing habit more cheaply than adding competitors, for Q-learning agents and for Qwen2.5-7B. Inside the model, the rival's price is linearly decodable, activation patching locates where it acts, and a steering vector moves the model's price far more than norm-matched random directions. A pre-registered test of whether it punishes undercutting was inconclusive (estimate −0.08, 95% CI −0.25 to 0.09, across 16 independent game histories; the 1,656 runs are repeated observations of those histories). Exploratory runs suggest it reacts to any change in the rival's price, not specifically to cuts. With Sriram Bharadwaj Peddinti and Chewon Cho.
  - dt: Limits
    dd: 48-hour sprint reports, not peer-reviewed. Small open models; the authors flag that more capable and reasoning models may behave differently.
side:
- status: Completed · reports and code public
  class: done
- text: Apart Research AI Collusion Research Sprint, Oct 23–25, 2026.
- links:
  - label: Peer-swap report ↗
    url: https://apartresearch.com/sprints/projects/noticing-the-move-missing-the-player-llm-agents-detect-behavioral-shifts-but-not-peer-swaps-uf7r
  - label: Pricing report ↗
    url: https://apartresearch.com/sprints/projects/tacit-collusion-in-pricing-agents-robustness-detection-and-a-mechanistic-probe-of-a-pricing-llm-qxsb
  - label: Code ↗
    url: https://github.com/Peddinti-Sriram-Bharadwaj/Collusion/tree/gagana/latent-manifold-steering
---
<p>Two projects from Apart Research's AI Collusion Research Sprint (October 2026). One asks whether colluding agents notice when a partner is swapped out; the other asks whether high prices set by an LLM pricing agent are actually evidence of a collusive strategy. Both come back to the same caution: what an agent does is easier to observe than why it does it.</p>
