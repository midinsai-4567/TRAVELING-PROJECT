import csv
import random

def get_recommendation(budget):
    recommendations = []

    with open("dataset/places.csv", newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if int(row["min_budget"]) <= budget <= int(row["max_budget"]):
                recommendations.append(row)

    if recommendations:
        choice = random.choice(recommendations)
        return choice["place"], choice["hotel"], choice["image"]
    else:
        return "No Place Found", "No Hotel Found"
