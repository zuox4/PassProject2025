import mysql.connector
from mysql.connector import Error
from collections import Counter, defaultdict

def get_class_from_db(class_name):
    connection = mysql.connector.connect(
        host='192.168.20.61',  # адрес сервера
        database='students',  # имя базы данных
        user='pass_system',  # имя пользователя
        password='ktSXPOr2ekCGS4cr'  # пароль

    )
    if connection.is_connected():
        cursor = connection.cursor()
        cursor.execute(f"SELECT * from students WHERE className='{class_name}' AND archive=0")
        record = cursor.fetchall()
        data = [{'name': i[3]+' '+i[2], 'className': i[5]} for i in record]
        for i in data:
            print(i)
        cursor.close()
        return data
    return None
def get_all_classes():
    connection = mysql.connector.connect(
        host='192.168.20.61',  # адрес сервера
        database='students',  # имя базы данных
        user='pass_system',  # имя пользователя
        password='ktSXPOr2ekCGS4cr'  # пароль

    )
    if connection.is_connected():
        cursor = connection.cursor()
        cursor.execute(f"SELECT className from students WHERE archive=0")
        record = cursor.fetchall()
        data = [i[0] for i in record]
        g = Counter(data)

        cursor.close()
        sorted_counter = dict(sorted(g.items(), key=lambda x: int(x[0].split('-')[0])))
        # d = defaultdict(list)
        # for class_name, count in sorted_counter.items():
        #     grade = int(class_name.split('-')[0])  # Извлекаем цифру класса
        #     d[grade].append((class_name, count))
        return sorted_counter
    return None
