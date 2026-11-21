def parse_event(line: str) -> dict:
    
    stripped = line.strip()
    if not stripped:
        raise ValueError("Пустая строка")

    # Строка делится не больше чем на 3 части по пробелам
    parts = stripped.split(" ", 2)
    if len(parts) != 3:
        raise ValueError("Строка должна содержать ровно три части: время, уровень и сообщение")

    time_str, level, message = parts
    valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR"}

    if level not in valid_levels:
        raise ValueError(f"Неизвестный или отсутствующий уровень логирования: '{level}'")

    return {
        "time": time_str,
        "level": level,
        "message": message
    }

def count_levels(lines) -> dict:
    """Считает, сколько строк каждого уровня встречается в последовательности строк.
    Испорченные строки учитываются под ключом 'BROKEN'.
    """
    counts = Counter()
    for line in lines:
        if not line.strip():
            continue
        try:
            event = parse_event(line)
            counts[event["level"]] += 1
        except ValueError:
            counts["BROKEN"] += 1
    return dict(counts)
