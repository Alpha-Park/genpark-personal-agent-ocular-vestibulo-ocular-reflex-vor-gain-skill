"""
MCP Server for Vestibulo-Ocular Reflex (VOR) Gain & Gaze Stabilization.
Exposes JSON-RPC endpoints for evaluating VOR impulse gain and bilateral canal asymmetry.
"""

import json
import sys
from client import VestibuloOcularReflexClient

client = VestibuloOcularReflexClient()


def handle_request(request: dict) -> dict:
    req_id = request.get("id")
    method = request.get("method")
    params = request.get("params", {})

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "evaluate_vor_gain",
                        "description": "Evaluates angular Vestibulo-Ocular Reflex (VOR) gain, presence of corrective catch-up saccades, and gaze stabilization index from head impulse data.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "head_velocity_deg_s": {"type": "number", "description": "Peak head impulse angular velocity in deg/s (e.g. 180.0)"},
                                "eye_velocity_deg_s": {"type": "number", "description": "Corresponding compensatory slow-phase eye velocity in deg/s (e.g. 172.0)"},
                                "canal_plane": {"type": "string", "default": "horizontal_lateral", "description": "Canal tested (horizontal_lateral, anterior, or posterior)"},
                                "has_covert_saccade": {"type": "boolean", "default": False, "description": "True if covert catch-up saccade occurred during head turn"},
                                "has_overt_saccade": {"type": "boolean", "default": False, "description": "True if overt catch-up saccade occurred after head turn"}
                            },
                            "required": ["head_velocity_deg_s", "eye_velocity_deg_s"]
                        }
                    },
                    {
                        "name": "compute_bilateral_canal_asymmetry",
                        "description": "Calculates percentage asymmetry between left and right semicircular canals to detect unilateral vestibular hypofunction.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "left_canal_gain": {"type": "number", "description": "Left canal VOR gain (e.g. 0.94)"},
                                "right_canal_gain": {"type": "number", "description": "Right canal VOR gain (e.g. 0.91)"}
                            },
                            "required": ["left_canal_gain", "right_canal_gain"]
                        }
                    }
                ]
            }
        }

    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "evaluate_vor_gain":
            res = client.evaluate_vor_gain(
                head_velocity_deg_s=args.get("head_velocity_deg_s", 180.0),
                eye_velocity_deg_s=args.get("eye_velocity_deg_s", 170.0),
                canal_plane=args.get("canal_plane", "horizontal_lateral"),
                has_covert_saccade=args.get("has_covert_saccade", False),
                has_overt_saccade=args.get("has_overt_saccade", False)
            )
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
            }

        elif tool_name == "compute_bilateral_canal_asymmetry":
            res = client.compute_bilateral_canal_asymmetry(
                left_canal_gain=args.get("left_canal_gain", 0.95),
                right_canal_gain=args.get("right_canal_gain", 0.92)
            )
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
            }

        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method {tool_name} not found"}
            }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32600, "message": "Invalid Request"}
    }


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
