# ♟️ RoboGambit  
### A Simulation & Hardware Robotics Challenge  
#### Developed by Sanidhya Ojha and Nitye Gupta
**ARIES × Robotics Club | 2025–2026 Edition**

RoboGambit is a two-phase robotics competition built around a chess-inspired mini-game played on a **6×6 board** using **two 4-DOF robotic arms**.

The competition mirrors real-world robotics workflows:

> Develop in Simulation → Validate → Deploy on Hardware

Participants must design an integrated system combining:
- 🧠 Autonomous Game Logic  
- 👁️ Vision-Based Perception (ArUco)  
- 🤖 Robotic Manipulation  
- 🔁 Human–Robot Collaboration  

---

# 🏁 Competition Structure

## Phase 1 — Simulation Stage (ROS 2 + Gazebo)

Teams develop and test their system in a simulated environment.

### Objective
- Implement full game reasoning logic  
- Detect and interpret board state using ArUco markers  
- Execute valid moves using a simulated robotic arm  
- Ensure reproducibility and robustness  

### Tech Stack
- ROS 2 Humble  
- Gazebo  
- Provided URDF + partial ROS workspace  
- Overhead camera model  

### Scoring
- Game Decision Model — 75 pts  
- Perception in Gazebo — 25 pts  

Qualification in this stage is required for the Hardware Stage.

---

## Phase 2 — Hardware Stage

The final competition is conducted on a physical arena.

### Hardware Platform
- 2 × Waveshare RoArm M2 (4-DOF arms)  
- Electromagnetic end-effector  
- ESP32 controller  
- Overhead camera (1920×1080 @ 30 FPS)  
- Fully ArUco-tagged arena  

Hardware modification is not permitted.

---

# 🔄 Hardware Competition Format

### 1️⃣ Timed Setup Phase  
Teams assemble the 6×6 board configuration using robotic arms.  
Seeding is determined based on completion time.

### 2️⃣ Collaborative Match Phase  
- 16-team double-elimination bracket  
- 1v1 matches  
- Alternating turns:
  - Human executes move
  - Robot autonomously perceives, reasons, and executes move  

Final standings are determined by match outcomes.

---

# 👥 Team Requirements

- Up to 10 members  
- Minimum 2 freshers (2025 batch)  
- All members from same hostel  
- One designated Point of Contact (PoC)  

Team remains same across both stages  
(+1 additional member allowed in hardware stage as human player)

---

# 📂 Repository Scope

This repository contains:

- Simulation resources  
- Task releases  
- Rule updates  
- Submission instructions  
- Reference materials  

Dedicated technical READMEs for Simulation and Hardware will be added separately.

---

# 📜 Official Rulebook

For complete rules and specifications, refer to the official rulebook included in this repository.

---

# 🚀 What RoboGambit Evaluates

- Full-stack robotics integration  
- Simulation-to-hardware transfer  
- Strategic decision-making  
- Robust perception pipelines  
- Safe and reliable manipulation  
- Human–robot collaboration  

---

**Organised by ARIES × Robotics Club**  
IIT Delhi | 2025–2026
