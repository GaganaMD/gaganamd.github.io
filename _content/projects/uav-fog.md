---
# Research project. Field guide: _content/projects/README.md
id: uav-fog
section: earlier
order: 2
tag: Optimisation · Edge–fog systems
title: Co-scheduling UAV routes and analytics across edge and fog
role: <strong>Paper:</strong> Suman Raj, Arindam Khanda, <strong>Gagana M D</strong>, Yogesh Simmhan, Sajal K. Das. <em>Mobility-Aware Cost-Efficient Co-Scheduling of UAV Routes and Analytics across Edge and Fog Computing.</em>
side:
- status: Research internship · IISc DREAM Lab
  class: done
- text: Jan – Aug 2025. DREAM Lab, led by Yogesh Simmhan.
---
<p>Drones used for crop monitoring and inspection need to run analytics such as DNN inference on what they capture. In rural areas there is little connectivity to offload that work. The idea here is to use rural transit buses, which increasingly carry compute and Wi-Fi hotspots, as <em>mobile</em> fog nodes. A drone can hand data to a passing bus, and the bus can compute on it or forward it once it reaches network coverage.</p>
<p>We formulated this as a Mission Scheduling Problem: choose drone flight paths that cover every task waypoint, and co-schedule each analytics task on board, on a static fog node, or on a bus, in line with bus timetables and task deadlines. Our Divide and Assign heuristic trades optimality for speed on large instances and is compared against the optimal solution. On real-world data it achieves 31–230% higher average utility than baselines and the state of the art, completes 100% of tasks across all workloads, and runs on the order of 10⁵ seconds faster than the optimal solver.</p>
<p>A secondary thread was reinforcement learning for split inference: deciding where to cut a model's layers between devices (ExpansionNet v2, YOLOv5).</p>
