from bs4 import BeautifulSoup
import psycopg2
from collections import defaultdict
from statistics import mean, median, variance
import os

DB_CONFIG = {
    'dbname': os.getenv('DB_NAME', 'colors'),
    'user': os.getenv('DB_USER', 'user'),
    'password': os.getenv('DB_PASSWORD', 'db_password'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432')
}

def parse_html(file_path: str) -> defaultdict:
    """
    Parse the HTML file and extract color frequencies.
    
    :param file_path: Path to the HTML file
    :return: Dictionary with color frequencies
    """
    color_set = defaultdict(int)
    
    with open(file_path, 'r') as file:
        soup = BeautifulSoup(file, features='html.parser')
        for row in soup.find_all('tr'):
            colors = row.select('td')[1].get_text().strip().replace('\n', '')
            for color in colors.split(', '):
                color_set[color.strip()] += 1
                
    return color_set

def calculate_statistics(color_set: defaultdict) -> dict:
    """
    Calculate various statistics from the color frequencies.
    
    :param color_set: Dictionary with color frequencies
    :return: Dictionary with calculated statistics
    """
    values = list(color_set.values())
    sorted_colors = sorted(color_set.items(), key=lambda item: item[1])
    stats = {
        'most_worn_color': max(color_set, key=color_set.get),
        'probability_red': color_set.get('RED', 0) / sum(values) if values else 0,
        'mean_color': sorted_colors[len(values) // 2][0],
        'median_color': sorted_colors[len(values) // 2][0] if len(values) % 2 != 0 else sorted_colors[len(values) // 2 - 1][0],
        'variance': variance(values)
    }
    return stats

def save_to_db(color_set: defaultdict):
    """
    Save the color frequencies to a PostgreSQL database.
    
    :param color_set: Dictionary with color frequencies
    """
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS colors (color VARCHAR PRIMARY KEY, frequency INT)"
    )
    for color, frequency in color_set.items():
        cursor.execute(
            "INSERT INTO colors (color, frequency) VALUES (%s, %s) "
            "ON CONFLICT (color) DO UPDATE SET frequency = EXCLUDED.frequency",
            (color, frequency)
        )
    
    conn.commit()
    cursor.close()
    conn.close()

def generate_result(file_path: str):
    """
    Generate and print the results.
    
    :param file_path: Path to the HTML file
    """
    color_set = parse_html(file_path)
    stats = calculate_statistics(color_set)
    # save_to_db(color_set)
    
    print(f"1. The mean color of the shirt is {stats['mean_color']}")
    print(f"2. The most worn color(s) is {stats['most_worn_color']}")
    print(f"3. The median color is {stats['median_color']}")
    print(f"4. The variance of the colors is {stats['variance']}")
    print(f"5. Probability of choosing a red color is {stats['probability_red']:.2f}")

if __name__ == '__main__':
    generate_result('webpage.html')
