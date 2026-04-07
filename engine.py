def calculate_stability(inf, exch, forex, intr, debt, stock):
    # This formula is from your project proposal!
    # Weights: Inflation 20%, Exchange 20%, Forex 20%, Interest 15%, Debt 15%, Stock 10%
    score = (inf * 0.20) + (exch * 0.20) + (forex * 0.20) + \
            (intr * 0.15) + (debt * 0.15) + (stock * 0.10)
    
    # Classification Logic
    if score <= 30:
        return round(score, 2), "Stable 🟢", "green"
    elif score <= 60:
        return round(score, 2), "Moderate Risk 🟡", "orange"
    else:
        return round(score, 2), "High Crisis Risk 🔴", "red"