from caskada import Node
from utils import fetch_recipes, call_llm_async, get_user_input

class FetchRecipes(Node):
    """Node that fetches recipes."""
    
    async def prep(self, shared):
        """Get ingredient from user."""
        ingredient = await get_user_input("Enter ingredient: ")
        return ingredient
    
    async def exec(self, ingredient):
        """Fetch recipes asynchronously."""
        recipes = await fetch_recipes(ingredient)
        return recipes
    
    async def post(self, shared, prep_res, recipes):
        """Store recipes and continue."""
        shared["recipes"] = recipes
        shared["ingredient"] = prep_res
        self.trigger("suggest")

class SuggestRecipe(Node):
    """Node that suggests a recipe using LLM."""
    
    async def prep(self, shared):
        """Get recipes from shared store."""
        return shared["recipes"]
    
    async def exec(self, recipes):
        """Get suggestion from LLM."""
        suggestion = await call_llm_async(
            f"Choose best recipe from: {', '.join(recipes)}"
        )
        return suggestion
    
    async def post(self, shared, prep_res, suggestion):
        """Store suggestion and continue."""
        shared["suggestion"] = suggestion
        self.trigger("approve")

class GetApproval(Node):
    """Node that gets user approval."""
    
    async def prep(self, shared):
        """Get current suggestion."""
        return shared["suggestion"]
    
    async def exec(self, suggestion):
        """Ask for user approval."""
        answer = await get_user_input(f"\nAccept this recipe? (y/n): ")
        return answer
    
    async def post(self, shared, prep_res, answer):
        """Handle user's decision."""
        if answer == "y":
            print("\nGreat choice! Here's your recipe...")
            print(f"Recipe: {shared['suggestion']}")
            print(f"Ingredient: {shared['ingredient']}")
            return self.trigger("accept")
            
        print("\nLet's try another recipe...")
        self.trigger("retry")