def check_zscore_alert(zscore, threshold):
    if abs(zscore) > threshold:
        return f"ALERT: Z-Score breached ({zscore:.2f})"
    return None
