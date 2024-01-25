def parse_comparison(latest, previous):
    delta = int((latest - previous) / latest * 100)
    if delta > 0:
        return f"{chr(0x1F53A)} {abs(delta)}% "  # Up arrow
    else:
        return f"{chr(0x1F53B)} {abs(delta)}%"  # Down arrow
    