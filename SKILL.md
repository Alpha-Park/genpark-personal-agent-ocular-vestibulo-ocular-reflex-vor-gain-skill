---
name: genpark-personal-agent-ocular-vestibulo-ocular-reflex-vor-gain-skill
description: Deterministic evaluation of angular Vestibulo-Ocular Reflex (VOR) gain, bilateral semicircular canal asymmetry, corrective saccades, and dynamic visual acuity.
version: 1.0.0
author: GenPark Autonomous Agents Ecosystem
license: MIT
tags:
  - personal-agent
  - ai-agent
  - openclaw
  - genpark
  - mcp
  - mcp-server
  - model-context-protocol
  - python
  - zero-dependency
  - wellness
  - productivity
  - production-ready
---

# Vestibulo-Ocular Reflex (VOR) Gain & Gaze Stabilization Skill

## Overview
The `genpark-personal-agent-ocular-vestibulo-ocular-reflex-vor-gain-skill` delivers neuro-otological gaze stabilization analytics to sovereign personal agents. The Vestibulo-Ocular Reflex (VOR) is a rapid three-neuron arc that maintains foveal target fixation by generating eye rotations equal and opposite to head acceleration. By processing head and eye angular velocity kinematics during rapid passive head impulses (vHIT), this skill calculates angular VOR gain, identifies compensatory covert/overt saccades, measures interaural canal asymmetry, and monitors dynamic visual acuity.

## Physiological Model & Mathematics
1. **Angular VOR Gain**:
   $$\text{VOR Gain} = \frac{|\dot{\theta}_{\text{eye}}|}{|\dot{\theta}_{\text{head}}|}$$
   - **Normative Physiological Window**: $0.85\text{ to }1.05$.
   - Deficits below $0.78$ lead to retinal slip, oscillopsia, and spatial disorientation.
2. **Bilateral Semicircular Canal Asymmetry**:
   $$\text{Asymmetry (\%)} = \frac{|\text{Gain}_L - \text{Gain}_R|}{\text{Gain}_L + \text{Gain}_R} \times 100\%$$
   - **Symmetric / Intact**: $< 8.0\%$.
   - **Unilateral Vestibular Loss**: $> 15.0\%$.
3. **Corrective Catch-Up Saccades**:
   - **Covert Saccades**: Generated while the head is still moving to minimize gaze position error.
   - **Overt Saccades**: Triggered post-movement; high diagnostic marker of deficient VOR slow-phase velocity.
4. **Vestibulo-Ocular Stability Index ($VOSI$)**:
   Synthesizes gain proximity to unity, absence of corrective saccades, and interaural balance into a 0 to 100 score.

## Tools & Endpoints
- `evaluate_vor_gain`: Evaluates impulse angular gain, catch-up saccade presence, and gaze stabilization index.
- `compute_bilateral_canal_asymmetry`: Calculates percentage asymmetry across contralateral canal pairs.
