import pandas as pd
import numpy as np

class MealSuggester:
    def __init__(self, data_path: str):
        self.df = pd.read_pickle(data_path)
        self._preprocess()

    def _preprocess(self):
        self.df = self.df[self.df['Calories'].notna()].copy()
        self.df['Calories'] = pd.to_numeric(self.df['Calories'], errors='coerce')
        self.df = self.df[self.df['Calories'].notna()]
        self.df = self.df.sort_values('Calories')

    def suggest_meal_options_greedy(self, target_cal, num_options=3, tolerance=50):
        found = []
        tried_sets = set()

        for _ in range(10):
            meal = self.df.sample(1)
            current_cal = meal['Calories'].values[0]

            remaining_cal = target_cal - current_cal
            second_options = self.df[(self.df['Calories'] <= remaining_cal + tolerance) & 
                                     (self.df['Calories'] >= remaining_cal - tolerance)]
            if second_options.empty:
                continue
            second = second_options.sample(1)
            current_cal += second['Calories'].values[0]

            remaining_cal = target_cal - current_cal
            third_options = self.df[(self.df['Calories'] <= remaining_cal + tolerance) & 
                                    (self.df['Calories'] >= remaining_cal - tolerance)]
            if third_options.empty:
                continue
            third = third_options.sample(1)

            selection = pd.concat([meal, second, third])
            total_cal = selection['Calories'].sum()
            ids = tuple(sorted(selection['RecipeId'].values))

            if ids not in tried_sets and abs(total_cal - target_cal) <= tolerance:
                found.append(selection)
                tried_sets.add(ids)

            if len(found) >= num_options:
                break

        return found

    def suggest(self, total_calories=2000, num_options_per_meal=3):
        targets = {
            'Bua sang': 0.35 * total_calories,
            'Bua trua': 0.35 * total_calories,
            'Bua toi': 0.30 * total_calories
        }
        result = {}

        for meal_name, target in targets.items():
            meal_options = self.suggest_meal_options_greedy(target, num_options=num_options_per_meal)
            result[meal_name] = []
            for meal in meal_options:
                recipes = []
                for _, row in meal.iterrows():
                  recipes.append({
    'RecipeId': int(row['RecipeId']),
    'Name': row['Name'],
    'CookTime': row['CookTime'],
    'PrepTime': row['PrepTime'],
    'TotalTime': row['TotalTime'],
    'Images': row['Images'],
    'RecipeCategory': row['RecipeCategory'],
    'RecipeIngredientQuantities': row['RecipeIngredientQuantities'],
    'RecipeIngredientParts': row['RecipeIngredientParts'],
    'Calories': float(row['Calories']),
    'FatContent': row['FatContent'],
    'CholesterolContent': row['CholesterolContent'],
    'SodiumContent': row['SodiumContent'],
    'CarbohydrateContent': row['CarbohydrateContent'],
    'FiberContent': row['FiberContent'],
    'SugarContent': row['SugarContent'],
    'ProteinContent': row['ProteinContent'],
    'RecipeInstructions': row['RecipeInstructions']  
})
                result[meal_name].append({
                    'TotalCalories': round(meal['Calories'].sum(), 1),
                    'Recipes': recipes
                })

        return result



