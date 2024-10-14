from pymongo import MongoClient
from bson.objectid import ObjectId


client = MongoClient("mongodb://localhost:27017/")
db = client["cats_db"]
collection = db["cats"]

# Функція додавання кота (імʼя, вік, характеристки)
def add_cat(name, age, features):
    try:
        cat = {"name": name, "age": age, "features": features}
        result = collection.insert_one(cat)
        print(f"Додано кота з ID: {result.inserted_id}")
    except Exception as e:
        print(f"Помилка при додаванні кота: {e}")


# Функція виводу всії котів в базі даних
def get_all_cats():
    try:
        cats = collection.find()
        for cat in cats:
            print(cat)
    except Exception as e:
        print(f"Помилка при виведенні котів: {e}")


# Вивід кота за імʼям
def get_cat_by_name(name):
    try:
        cat = collection.find_one({"name": name})
        if cat:
            print(cat)
        else:
            print(f"Кіт з ім'ям {name} не знайдений")
    except Exception as e:
        print(f"Помилка при пошуку кота: {e}")


# Функція зміни віку кота за імʼям
def update_cat_age(name, new_age):
    try:
        result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
        if result.matched_count > 0:
            print(f"Вік кота {name} оновлено до {new_age}")
        else:
            print(f"Кіт з ім'ям {name} не знайдений")
    except Exception as e:
        print(f"Помилка при оновленні віку кота: {e}")


# Функція зміни характеристики кота за імʼям
def add_feature_to_cat(name, feature):
    try:
        result = collection.update_one({"name": name}, {"$push": {"features": feature}})
        if result.matched_count > 0:
            print(f"Характеристика '{feature}' додана коту {name}")
        else:
            print(f"Кіт з ім'ям {name} не знайдений")
    except Exception as e:
        print(f"Помилка при додаванні характеристики: {e}")


# Видалення кота з бази за імʼям
def delete_cat_by_name(name):
    try:
        result = collection.delete_one({"name": name})
        if result.deleted_count > 0:
            print(f"Кіт з ім'ям {name} видалений")
        else:
            print(f"Кіт з ім'ям {name} не знайдений")
    except Exception as e:
        print(f"Помилка при видаленні кота: {e}")


# Функція видалення всіх котів
def delete_all_cats():
    try:
        result = collection.delete_many({})
        print(f"Видалено {result.deleted_count} котів")
    except Exception as e:
        print(f"Помилка при видаленні всіх котів: {e}")


def menu():
    print("\nМеню:")
    print("1. Додати кота")
    print("2. Показати всіх котів")
    print("3. Знайти кота за ім'ям")
    print("4. Оновити вік кота")
    print("5. Додати характеристику коту")
    print("6. Видалити кота за ім'ям")
    print("7. Видалити всіх котів")
    print("0. Вихід")


if __name__ == "__main__":
    while True:
        menu()
        choice = input("\nВиберіть опцію: ")

        if choice == "1":
            name = input("Введіть ім'я кота: ")
            age = int(input("Введіть вік кота: "))
            features = input("Введіть характеристики (через кому): ").split(", ")
            add_cat(name, age, features)

        elif choice == "2":
            print("\nСписок всіх котів:")
            get_all_cats()

        elif choice == "3":
            name = input("Введіть ім'я кота: ")
            get_cat_by_name(name)

        elif choice == "4":
            name = input("Введіть ім'я кота, якому потрібно оновити вік: ")
            new_age = int(input("Введіть новий вік: "))
            update_cat_age(name, new_age)

        elif choice == "5":
            name = input("Введіть ім'я кота: ")
            feature = input("Введіть нову характеристику: ")
            add_feature_to_cat(name, feature)

        elif choice == "6":
            name = input("Введіть ім'я кота, якого потрібно видалити: ")
            delete_cat_by_name(name)

        elif choice == "7":
            confirm = input("Ви впевнені, що хочете видалити всіх котів? (y/n): ")
            if confirm.lower() == "y":
                delete_all_cats()

        elif choice == "0":
            print("Вихід з програми...")
            break

        else:
            print("Невірний вибір. Спробуйте ще раз.")