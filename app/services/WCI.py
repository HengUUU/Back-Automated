def compute_wci(avg_param: dict) -> float:
    """
    Compute Water Criticality Index (WCI) for a single factory.
    Higher WCI means higher environmental risk.
    """
    # Handle None values
    ph = avg_param.get("ph")
    cod = avg_param.get("cod")
    ss = avg_param.get("ss")

    # pH score: 0 if within safe range, up to 1 if far outside
    if ph is None:
        ph_score = 0
    elif 5.5 <= ph <= 9:
        ph_score = 0  # safe
    elif ph < 5.5:
        ph_score = min((5.5 - ph) / 5.5, 1)
    else:  # ph > 9
        ph_score = min((ph - 9) / 9, 1)

    # COD score: 0 if < 120, up to 1 if very high
    if cod is None or cod<120:
        cod_score = 0
    else:
        cod_score = min(cod / 120, 1)

    # SS score: 0 if < 100, up to 1 if very high
    if ss is None or ss <100:
        ss_score = 0
    else:
        ss_score = min(ss / 100, 1)

    # Weighted sum (equal weight for now)
    wci = (ph_score + cod_score + ss_score) / 3 * 100  # scale 0-100
    return round(wci, 2)
