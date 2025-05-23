from utils import replace_nan_with_none
from fastapi import FastAPI, Request, Query
from fastapi.responses import JSONResponse
from meal_suggester import MealSuggester
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
 
suggester = MealSuggester('recipes_with_embeddings.pkl')

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://hcmute-care.id.vn",
        "https://www.hcmute-care.id.vn",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/suggest-meals/{calories}")
async def suggest_meals_api(calories: int, num_options: int = Query(2)):
    try:
        result = suggester.suggest(total_calories=calories, num_options_per_meal=num_options)
        dt = replace_nan_with_none(result)
        return dt
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})




# from flask import Flask, jsonify, request
# from meal_suggester import MealSuggester

# app = Flask(__name__)

# suggester = MealSuggester('recipes_with_embeddings.pkl')

# @app.route('/api/suggest-meals/<int:calories>', methods=['POST'])
# def suggest_meals_api(calories):
#     try:
#         num_options = int(request.args.get('num_options', 2))

#         result = suggester.suggest(total_calories=calories, num_options_per_meal=num_options)
#         return jsonify(result)
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)
