def compute_p_total(p_step_percent, n):
    try:
        p_step = float(p_step_percent) / 100.0
        n = float(n)
        p_total = 100 * (p_step ** n)
        return round(p_total, 3)
    except (ValueError, ZeroDivisionError):
        return "Invalid"