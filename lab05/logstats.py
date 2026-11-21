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

def top_errors(lines, n: int) -> list:
    """Возвращает n самых частых сообщений уровня ERROR в виде пар [сообщение, сколько раз].
    При равенстве сортировка происходит по алфавиту сообщений.
    """
    error_messages = []
    for line in lines:
        if not line.strip():
            continue
        try:
            event = parse_event(line)
            if event["level"] == "ERROR":
                error_messages.append(event["message"])
        except ValueError:
            continue

    # Считаем количество каждой ошибки
    freq = Counter(error_messages)

    sorted_errors = sorted(freq.items(), key=lambda item: (-item[1], item[0]))

    # Возвращаем список пар в виде списков [сообщение, количество]
    return [[msg, count] for msg, count in sorted_errors[:n]]

def format_report(counts: dict, errors: list) -> str:
    """Формирует текст отчёта по готовым подсчётам.
    Уровни выводятся по алфавиту, в конце текста перевод строки.
    """
    lines_out = ["Отчёт по журналу\n"]

    # Уровни сортируем по алфавиту (включая BROKEN, если он есть)
    sorted_levels = sorted(counts.keys())
    for lvl in sorted_levels:
        lines_out.append(f"{lvl}: {counts[lvl]}")

    lines_out.append("\nЧастые ошибки:")
    if not errors:
        lines_out.append("- Нет зафиксированных ошибок уровня ERROR")
    else:
        for msg, count in errors:
            lines_out.append(f"- {msg} — {count}")

    # Собираем всё через перевод строки, гарантируя завершающий \n в конце
    return "\n".join(lines_out) + "\n"
