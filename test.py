import psycopg2
import random
from datetime import datetime

# Параметры подключения к базе данных(для безопастности оставлены пустыми)
conn = psycopg2.connect(
    host="",
    database="",
    user="",
    password=""
)

# Функция для генерации случайного статуса дрона
def generate_status(drone_id):
    battery_level = round(random.uniform(5.0, 100.0), 2)  # Уровень заряда от 5 до 100
    signal_strength = round(random.uniform(0.0, 100.0), 2)  # Мощность сигнала от 0 до 100
    x_coordinate = round(random.uniform(-1000.0, 1000.0), 2)  # X-координата от -1000 до 1000
    y_coordinate = round(random.uniform(-1000.0, 1000.0), 2)  # Y-координата от -1000 до 1000
    z_coordinate = round(random.uniform(0.0, 500.0), 2)  # Z-координата от 0 до 500
    timestamp = datetime.now()  # Текущее время
    
    return (drone_id, battery_level, signal_strength, x_coordinate, y_coordinate, z_coordinate, timestamp)

# Функция для вставки данных в таблицу Status_Dron
def insert_status(cursor, status_data):
    query = """
        INSERT INTO Status_Dron (Drone_Number, Battery_Level, Signal_Strength, X_Coordinate, Y_Coordinate, Z_Coordinate, Timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, status_data)

# Генерация и добавление данных для всех дронов
def generate_and_insert_statuses():
    with conn.cursor() as cursor:
        # Получаем список всех ID дронов
        cursor.execute("SELECT ID FROM Dron")
        drones = cursor.fetchall()

        # Генерация случайного статуса для каждого дрона
        for drone in drones:
            status_data = generate_status(drone[0])
            insert_status(cursor, status_data)
        
        # Подтверждаем изменения
        conn.commit()

# Запускаем генерацию и вставку данных
if __name__ == "__main__":
    try:
        generate_and_insert_statuses()
        print("Successfully")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()
