"""Database params"""
DB_FILE_NAME = 'open_weather_history.db'
TABLE_NAME = 'weather'
TABLE_COLUMNS = {
    'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
    'dt': 'TEXT',
    'city_name': 'TEXT',
    'description': 'TEXT',
    'temp': 'REAL',
    'feels_like': 'REAL',
    'wind_speed': 'REAL'
}
