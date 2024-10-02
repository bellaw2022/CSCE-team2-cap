import React, { useState } from 'react';

const RecipeRecommendationPage = () => {
    const [recipes, setRecipes] = useState([]);
    const [creativeRecipe, setCreativeRecipe] = useState('');
    const [ingredients, setIngredients] = useState('');

    const handleGetRecipes = async () => {
        const response = await fetch('https://api.spoonacular.com/recipes/findByIngredients?ingredients=apple,banana');
        const data = await response.json();
        setRecipes(data);
    };

    const handleGetCreativeRecipes = async () => {
        try {
            setCreativeRecipe(''); // Clear previous recipe
            const response = await fetch('http://127.0.0.1:5000/api/gpt-creative-recipe', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    ingredients: ingredients.split(',').map(ingredient => ingredient.trim()),
                })
            });
            
            if (!response.ok) {
                // Handle error
                console.error('Error:', response.statusText);
                return;
            }

            const reader = response.body.getReader();
            const decoder = new TextDecoder('utf-8');
            let done = false;

            while (!done) {
                const { value, done: doneReading } = await reader.read();
                done = doneReading;
                if (value) {
                    const chunk = decoder.decode(value);
                    // Process SSE formatted chunk
                    const lines = chunk.split('\n\n');
                    for (let line of lines) {
                        if (line.startsWith('data: ')) {
                            const data = line.slice(6);
                            if (data.startsWith('{"error":')) {
                                // Handle error message
                                console.error('Error:', JSON.parse(data).error);
                            } else {
                                // Update the creative recipe text
                                setCreativeRecipe(prev => prev + data);
                            }
                        }
                    }
                }
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <div>
            <h2>Recipe Recommendation</h2>
            <div>
                <button onClick={handleGetRecipes}>Get Recipes from API</button>
                <ul>
                    {recipes.map((recipe) => (
                        <li key={recipe.id}>{recipe.title}</li>
                    ))}
                </ul>
            </div>

            <div>
                <h3>Creative Recipe (by GPT)</h3>
                <input
                    type="text"
                    value={ingredients}
                    onChange={(e) => setIngredients(e.target.value)}
                    placeholder="Enter ingredients separated by commas"
                />
                <button onClick={handleGetCreativeRecipes}>Get Creative Recipe</button>
                <p>{creativeRecipe}</p>
            </div>
        </div>
    );
};

export default RecipeRecommendationPage;
