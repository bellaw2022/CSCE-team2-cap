from flask import Blueprint, jsonify, request, Response
import requests
import openai
import os

recipe_route = Blueprint('recipe_route', __name__)

@recipe_route.route('/api/get-recipe', methods=['GET'])
async def get_recipe():
    # Fetch from external recipe API
    response = requests.get('https://api.spoonacular.com/recipes/findByIngredients?ingredients=apple,banana&apiKey=YOUR_SPOONACULAR_API_KEY')
    data = response.json()
    return jsonify(data)

@recipe_route.route('/api/gpt-creative-recipe', methods=['POST'])
async def generate_recipe():
    if request.content_type != 'application/json':
        return jsonify({"error": "Unsupported Media Type"}), 415

    data = request.get_json() or {}
    ingredients = data.get('ingredients', [])

    if not ingredients:
        return jsonify({"error": "No ingredients provided"}), 400

    def generate():
        try:
            openai.api_key = os.getenv('OPENAI_API_KEY')
            if not openai.api_key:
                yield 'data: {"error": "OpenAI API key not set"}\n\n'
                return

            prompt = f"""
                Generate a recipe given the following ingredients:
                {"\n- ".join(ingredients)}\n
                Keep the directions simple and easy to follow.
            """

            stream = openai.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a recipe bot."},
                    {"role": "user", "content": prompt}
                ],
                model="gpt-4o",
                stream=True
            )

            for chunk in stream:
                if chunk.choices[0].delta.role == "system":
                    continue
                content = chunk.choices[0].delta.content
                print(content, end='')
                yield f'data: {content}\n\n'
        except Exception as e:
            yield f'data: {{"error": "{str(e)}"}}\n\n'

    return Response(generate(), mimetype='text/event-stream')