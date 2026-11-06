import sys
from stats import average_by_city, read_valid, warmest_city

def main():
    lines = sys.stdin.read().splitlines()
    
    # Считаем количество непустых строк для определения числа ошибок
    non_empty_count = sum(1 for line in lines if line.strip())
    
    valid_records = read_valid(lines)
    parsed_count = len(valid_records)
    skipped_count = non_empty_count - parsed_count
    
    avgs = average_by_city(valid_records)
    warmest = warmest_city(valid_records)
    
    print(parsed_count)
    print(skipped_count)
    if warmest and warmest in avgs:
        print(f"{avgs[warmest]:.1f}")
    else:
        print("0.0")

if __name__ == "__main__":
    main()
