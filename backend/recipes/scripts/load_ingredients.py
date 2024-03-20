import csv
import os
import django
from recipes.models import Ingredient

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

# Определите корень проекта (FOODRAM)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Путь к файлу ingredients.csv относительно корня проекта
csv_file_path = os.path.join(BASE_DIR, 'data/ingredients.csv')

# Проверяем, что файл существует
if not os.path.isfile(csv_file_path):
    raise FileNotFoundError(f"File not found: {csv_file_path}")


def load_ingredients_from_csv(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            ingredient = Ingredient(
                name=row['name'],
                measurement_unit=row['measurement_unit']
            )
            ingredient.save()


if __name__ == '__main__':
    load_ingredients_from_csv(csv_file_path)
