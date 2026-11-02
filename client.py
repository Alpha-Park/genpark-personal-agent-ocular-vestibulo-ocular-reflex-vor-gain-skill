"""
Vestibulo-Ocular Reflex (VOR) Gain & Gaze Stabilization Engine.
Provides deterministic, zero-dependency modeling of angular VOR gain,
bilateral semicircular canal asymmetry, corrective catch-up saccades, and dynamic visual acuity.
"""

from typing import Dict, Any, List, Optional


class VestibuloOcularReflexClient:
    """
    Deterministic client for analyzing Vestibulo-Ocular Reflex (VOR) impulses and gaze stabilization.
    Pure Python standard library implementation based on Curthoys & Halmagyi vHIT neuro-otology standards.
    """

    def __init__(self):
        pass

    def evaluate_vor_gain(
        self,
        head_velocity_deg_s: float,
        eye_velocity_deg_s: float,
        canal_plane: str = "horizontal_lateral",
        has_covert_saccade: bool = False,
        has_overt_saccade: bool = False
    ) -> Dict[str, Any]:
        """
        Evaluates single-direction VOR gain from head impulse test.
        VOR Gain = Eye Velocity / Head Velocity.
        Ideal physiological gain is ~ 0.85 to 1.05 for horizontal canals.
        """
        if abs(head_velocity_deg_s) < 50.0:
            return {"error": "Head velocity must exceed 50 deg/s for diagnostic impulse validity"}

        gain = round(abs(eye_velocity_deg_s) / abs(head_velocity_deg_s), 3)

        # Catch-up saccade penalty: corrective saccades confirm inadequate slow-phase VOR velocity
        saccade_penalty = 0.0
        if has_covert_saccade:
            saccade_penalty += 15.0
        if has_overt_saccade:
            saccade_penalty += 20.0

        # Normal gain target: 0.85 to 1.05
        if 0.85 <= gain <= 1.05:
            gain_score = 50.0
        elif gain < 0.85:
            gain_score = max(5.0, 50.0 - (0.85 - gain) * 80.0)
        else:
            # Hyper-gain (e.g. cerebellar disinhibition)
            gain_score = max(10.0, 50.0 - (gain - 1.05) * 60.0)

        vosi_score = round(max(5.0, min(100.0, gain_score * 2.0 - saccade_penalty)), 1)

        is_hypofunction = gain < 0.78 or has_overt_saccade

        if vosi_score >= 80.0:
            status = "OPTIMAL_GAZE_STABILIZATION"
            interpretation = f"Normal physiological VOR gain ({gain}) in {canal_plane} plane; sharp retinal image lock during rapid head turn."
            guidance = "Vestibular ocular pathway is intact. Full dynamic visual acuity preserved during high-speed motion."
        elif is_hypofunction:
            status = "VESTIBULAR_HYPOFUNCTION_DEFICIT"
            interpretation = f"Attenuated VOR gain ({gain}) with compensatory catch-up saccades. Suggests peripheral vestibular hypofunction or labyrinthine fatigue."
            guidance = "Gaze slip present. Perform VOR x1 adaptation drills (fixating on stationary target while oscillating head at 2 Hz)."
        else:
            status = "MILD_VOR_ATTENUATION"
            interpretation = f"Borderline VOR gain ({gain}); minor gaze instability under high rotational acceleration."
            guidance = "Incorporate vestibular-ocular coordination exercises and monitor motion sickness sensitivity."

        return {
            "canal_plane": canal_plane,
            "head_velocity_deg_s": head_velocity_deg_s,
            "eye_velocity_deg_s": eye_velocity_deg_s,
            "vor_gain": gain,
            "has_covert_saccade": has_covert_saccade,
            "has_overt_saccade": has_overt_saccade,
            "vestibulo_ocular_stability_index": vosi_score,
            "status": status,
            "physiological_interpretation": interpretation,
            "actionable_guidance": guidance
        }

    def compute_bilateral_canal_asymmetry(
        self,
        left_canal_gain: float,
        right_canal_gain: float
    ) -> Dict[str, Any]:
        """
        Calculates bilateral semicircular canal asymmetry percentage:
        Asymmetry (%) = |Gain_L - Gain_R| / (Gain_L + Gain_R) * 100.
        Normative threshold is < 8-10%. Asymmetry > 15% indicates unilateral vestibular hypofunction.
        """
        total_gain = left_canal_gain + right_canal_gain
        if total_gain <= 0:
            return {"error": "Sum of left and right gains must be positive"}

        asym_pct = round((abs(left_canal_gain - right_canal_gain) / total_gain) * 100.0, 1)

        if asym_pct <= 8.0:
            tier = "SYMMETRIC_BILATERAL_VESTIBULAR_TONE"
            notes = "Balanced bilateral vestibular inputs; zero rotational velocity drift or spontaneous nystagmus risk."
        elif asym_pct <= 15.0:
            tier = "MILD_INTERAURAL_ASYMMETRY"
            notes = "Mild interaural asymmetry; central vestibular compensation is generally able to adapt."
        else:
            tier = "MARKED_UNILATERAL_VESTIBULAR_ASYMMETRY"
            notes = f"Significant interaural canal imbalance ({asym_pct}%). Likely unilateral vestibular loss or acute asymmetric labyrinthine impairment."

        return {
            "left_canal_gain": left_canal_gain,
            "right_canal_gain": right_canal_gain,
            "bilateral_asymmetry_pct": asym_pct,
            "classification": tier,
            "clinical_notes": notes
        }
