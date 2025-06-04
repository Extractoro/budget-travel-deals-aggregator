def safe_strip(selector):
    text = selector.get()
    return text.strip() if text else None
