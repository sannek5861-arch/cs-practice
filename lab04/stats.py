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
        
    return {"city": city, "temp": temp, "date": date}
