# Vestibulo-Ocular Reflex (VOR) Gain & Gaze Stabilization Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen.svg)](https://github.com/alphaparkinc/genpark-personal-agent-ocular-vestibulo-ocular-reflex-vor-gain-skill)
[![OpenClaw Ready](https://img.shields.io/badge/OpenClaw-Compatible-purple.svg)](https://github.com/alphaparkinc/genpark-personal-agent-ocular-vestibulo-ocular-reflex-vor-gain-skill)
[![MCP Protocol](https://img.shields.io/badge/MCP-Standard-orange.svg)](https://modelcontextprotocol.io/)

A sovereign personal agent capability for computational neuro-otology, evaluating angular Vestibulo-Ocular Reflex (VOR) gain, bilateral semicircular canal asymmetry, and dynamic visual acuity.

## Architecture

```mermaid
flowchart TD
    ImpulseData["Head Impulse Kinematics: Head Velocity & Eye Velocity (deg/s)"] --> GainEngine["VOR Gain Engine = abs(Eye Velocity) / abs(Head Velocity)"]
    GainEngine --> SaccadeAudit["Corrective Saccade Audit (Covert vs Overt Retinal Slip)"]
    GainEngine --> AsymmetryCalc["Contralateral Canal Asymmetry: |Gain_L - Gain_R| / (Gain_L + Gain_R) * 100%"]
    SaccadeAudit & AsymmetryCalc --> VOSI["Vestibulo-Ocular Stability Index (VOSI: 0 - 100)"]
    VOSI --> TherapyPlan["OpenClaw / Hermes Vestibular Adaptation (VOR x1) Prescriptions"]
```

## Quickstart

```python
from client import VestibuloOcularReflexClient

client = VestibuloOcularReflexClient()

# Assess horizontal canal head impulse test (vHIT)
res = client.evaluate_vor_gain(
    head_velocity_deg_s=195.0,
    eye_velocity_deg_s=184.0,
    canal_plane="horizontal_lateral",
    has_covert_saccade=False,
    has_overt_saccade=False
)

print("VOR Gain:", res["vor_gain"])
print("Stability Index:", res["vestibulo_ocular_stability_index"], "/ 100")
print("Status:", res["status"])
```

## MCP Server Integration

Add to your `claude_desktop_config.json` or OpenClaw tool registry:

```json
{
  "mcpServers": {
    "vor-gain": {
      "command": "python",
      "args": ["/path/to/genpark-personal-agent-ocular-vestibulo-ocular-reflex-vor-gain-skill/mcp_server.py"]
    }
  }
}
```

## License
MIT License.
