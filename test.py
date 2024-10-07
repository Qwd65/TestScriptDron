import psycopg2
import random
from datetime import datetime

# Параметры подключения к базе данных (для безопасности оставлены пустыми)
conn = psycopg2.connect(
    host="",
    database="",
    user="",
    password=""
)

# Функция для генерации случайного статуса дрона
def generate_status(drone_id, current_coordinates):
    battery_level = round(random.uniform(5.0, 100.0), 2)  
    signal_strength = round(random.uniform(5.0, 100.0), 2)  
    
  
    x_offset = round(random.uniform(-5.0, 5.0), 2)
    y_offset = round(random.uniform(-5.0, 5.0), 2)
    z_offset = round(random.uniform(-1.0, 1.0), 2)  

    x_coordinate = round(current_coordinates[0] + x_offset, 2)
    y_coordinate = round(current_coordinates[1] + y_offset, 2)
    z_coordinate = round(current_coordinates[2] + z_offset, 2)

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
        # Получаем список всех ID дронов и их текущие координаты
        cursor.execute("SELECT ID, X_Coordinate, Y_Coordinate, Z_Coordinate FROM Dron")
        drones = cursor.fetchall()

        # Генерация случайного статуса для каждого дрона
        for drone in drones:
            drone_id = drone[0]
            current_coordinates = (drone[1], drone[2], drone[3])
            status_data = generate_status(drone_id, current_coordinates)
            insert_status(cursor, status_data)
    
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
