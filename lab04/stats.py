def parse_record(line: str) -> dict:
    """Разбирает строку «город;температура;дата» в словарь.
    Вызывает ValueError при некорректных данных.
    """
    parts = line.split(";")
    if len(parts) != 3:
        raise ValueError("Строка должна содержать ровно три поля, разделенных точкой с запятой")
    
    city, temp_str, date = parts
    city = city.strip()
    date = date.strip()
    
    if not city or not date:
        raise ValueError("Город и дата не могут быть пустыми")
    
    try:
        temp = float(temp_str)
    except ValueError:
        raise ValueError(f"Некорректное значение температуры: '{temp_str}'")
        
    return {"city": city, "temperature": temp, "date": date}

def read_valid(lines: list[str]) -> list[dict]:
    """Разбирает строки журнала, пропуская пустые и негодные строки."""
    records = []
    for line in lines:
        if not line.strip():
            continue
        try:
            record = parse_record(line)
            records.append(record)
        except ValueError:
            pass
    return records

def average_by_city(records: list[dict]) -> dict:
    """Считает среднюю температуру по каждому городу, округляя до десятых."""
    totals = {}
    counts = {}
    for r in records:
        city = r["city"]
        temp = r["temperature"]
        totals[city] = totals.get(city, 0.0) + temp
        counts[city] = counts.get(city, 0) + 1
        
    averages = {}
    for city in totals:
        averages[city] = round(totals[city] / counts[city], 1)
    return averages

def warmest_city(records: list[dict]) -> str:
    """Находит самый тёплый город. При равенстве температур выбирает первый по алфавиту."""
    if not records:
        return ""
    avgs = average_by_city(records)
    if not avgs:
        return ""
    
    # Сортировка по убыванию температуры, затем по возрастанию имени города (алфавит)
    sorted_cities = sorted(avgs.items(), key=lambda x: (-x[1], x[0]))
    return sorted_cities[0][0]
