"""
Example usage for Vestibulo-Ocular Reflex (VOR) Gain Skill.
Demonstrates analyzing head impulse gaze stabilization and bilateral canal asymmetry.
"""

from client import VestibuloOcularReflexClient


def main():
    client = VestibuloOcularReflexClient()

    print("=== 1. Evaluating Left Lateral Canal VOR Gain (vHIT) ===")
    res_left = client.evaluate_vor_gain(
        head_velocity_deg_s=195.0,
        eye_velocity_deg_s=184.0,
        canal_plane="horizontal_lateral",
        has_covert_saccade=False,
        has_overt_saccade=False
    )
    print(f"Head Velocity: {res_left['head_velocity_deg_s']} deg/s | Eye Velocity: {res_left['eye_velocity_deg_s']} deg/s")
    print(f"VOR Gain: {res_left['vor_gain']} (Normative: 0.85 - 1.05)")
    print(f"Covert Saccades: {res_left['has_covert_saccade']} | Overt Saccades: {res_left['has_overt_saccade']}")
    print(f"Stability Index: {res_left['vestibulo_ocular_stability_index']} / 100")
    print(f"Status: {res_left['status']}")
    print(f"Interpretation: {res_left['physiological_interpretation']}")
    print(f"Guidance: {res_left['actionable_guidance']}")

    print("\n=== 2. Evaluating Bilateral Semicircular Canal Asymmetry ===")
    asym_res = client.compute_bilateral_canal_asymmetry(
        left_canal_gain=0.94,
        right_canal_gain=0.90
    )
    print(f"Left Gain: {asym_res['left_canal_gain']} | Right Gain: {asym_res['right_canal_gain']}")
    print(f"Bilateral Asymmetry: {asym_res['bilateral_asymmetry_pct']} % (Normative: < 8-10%)")
    print(f"Classification: {asym_res['classification']}")
    print(f"Clinical Notes: {asym_res['clinical_notes']}")


if __name__ == "__main__":
    main()
