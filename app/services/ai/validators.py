from app.services.ai.equipment_catalog import match_equipment_key


def validate_equipment(ai_output: dict):
    equipment = ai_output.get("equipment")
    if equipment is None:
        return None
    e = str(equipment).strip().lower().replace("’", "'")
    if e == "unknown":
        return None
    key = match_equipment_key(e)
    if not key:
        return None
    return {**ai_output, "equipment": key}


def validate_food_items(items: list):
    valid_items = []
    food_synonyms = {
        "apple": ["apple", "apples"],
        "banana": ["banana", "bananas"],
        "chicken": ["chicken", "chicken breast", "chicken thigh", "chicken wing"],
        "rice": ["rice", "white rice", "brown rice", "steamed rice"],
        "broccoli": ["broccoli", "broccoli florets"],
        "egg": ["egg", "eggs", "boiled egg", "fried egg", "scrambled egg"],
        "bread": ["bread", "toast", "sandwich bread", "whole wheat bread"],
        "yogurt": ["yogurt", "greek yogurt", "plain yogurt"],
        "salmon": ["salmon", "salmon fillet", "smoked salmon"],
        "pasta": ["pasta", "spaghetti", "penne", "macaroni", "noodles"],
        "orange": ["orange", "oranges"],
        "grapes": ["grapes", "grape"],
        "strawberry": ["strawberry", "strawberries"],
        "blueberry": ["blueberry", "blueberries"],
        "watermelon": ["watermelon", "watermelon slice"],
        "pineapple": ["pineapple", "pineapple chunks"],
        "mango": ["mango", "mangoes"],
        "avocado": ["avocado", "avocados", "guacamole"],
        "tomato": ["tomato", "tomatoes", "cherry tomatoes"],
        "cucumber": ["cucumber", "cucumbers"],
        "lettuce": ["lettuce", "romaine lettuce", "iceberg lettuce"],
        "spinach": ["spinach", "baby spinach"],
        "carrot": ["carrot", "carrots", "baby carrots"],
        "potato": ["potato", "potatoes", "baked potato", "mashed potatoes"],
        "sweet potato": ["sweet potato", "sweet potatoes", "yam"],
        "onion": ["onion", "onions", "red onion", "white onion"],
        "garlic": ["garlic", "garlic cloves"],
        "bell pepper": ["bell pepper", "peppers", "green pepper", "red pepper", "yellow pepper"],
        "beef": ["beef", "steak", "ground beef", "beef patty"],
        "pork": ["pork", "pork chop", "pork loin", "bacon"],
        "turkey": ["turkey", "turkey breast", "ground turkey"],
        "fish": ["fish", "fish fillet", "grilled fish"],
        "tuna": ["tuna", "tuna salad", "canned tuna"],
        "shrimp": ["shrimp", "prawns"],
        "cheese": ["cheese", "cheddar", "mozzarella", "swiss cheese"],
        "milk": ["milk", "dairy milk", "whole milk"],
        "butter": ["butter", "margarine"],
        "olive oil": ["olive oil", "extra virgin olive oil"],
        "honey": ["honey", "raw honey"],
        "sugar": ["sugar", "white sugar", "brown sugar"],
        "salt": ["salt", "table salt"],
        "pepper": ["pepper", "black pepper"],
        "coffee": ["coffee", "espresso", "cappuccino"],
        "tea": ["tea", "green tea", "black tea"],
        "water": ["water", "bottled water"],
        "juice": ["juice", "orange juice", "apple juice"],
        "soda": ["soda", "pop", "soft drink", "cola"],
        "beer": ["beer", "ale", "lager"],
        "wine": ["wine", "red wine", "white wine"],
        "chocolate": ["chocolate", "dark chocolate", "milk chocolate"],
        "ice cream": ["ice cream", "gelato"],
        "cake": ["cake", "birthday cake", "chocolate cake"],
        "cookie": ["cookie", "cookies", "chocolate chip cookie"],
        "chips": ["chips", "potato chips", "crisps"],
        "pretzel": ["pretzel", "pretzels"],
        "popcorn": ["popcorn", "popcorn kernels"],
        "nuts": ["nuts", "mixed nuts"],
        "almonds": ["almonds", "almond"],
        "walnuts": ["walnuts", "walnut"],
        "peanuts": ["peanuts", "peanut"],
        "cashews": ["cashews", "cashew"],
        "pizza": ["pizza", "pizza slice", "pepperoni pizza"],
        "burger": ["burger", "hamburger", "cheeseburger"],
        "sandwich": ["sandwich", "sub", "hoagie"],
        "salad": ["salad", "green salad", "caesar salad"],
        "soup": ["soup", "vegetable soup", "chicken soup"],
        "cereal": ["cereal", "breakfast cereal", "oat cereal"],
        "oatmeal": ["oatmeal", "porridge"],
        "pancake": ["pancake", "pancakes", "flapjack"],
        "waffle": ["waffle", "waffles"],
        "bacon": ["bacon", "strip of bacon"],
        "sausage": ["sausage", "sausages", "breakfast sausage"],
        "hot dog": ["hot dog", "hotdog", "frankfurter"],
        "fries": ["fries", "french fries", "potato fries"],
        "nachos": ["nachos", "nachos chips"],
        "taco": ["taco", "tacos", "hard taco", "soft taco"],
        "burrito": ["burrito", "burritos", "wrap"],
        "quesadilla": ["quesadilla", "cheese quesadilla"],
        "sushi": ["sushi", "sushi roll", "maki"],
        "ramen": ["ramen", "ramen noodles"],
        "stir fry": ["stir fry", "stir-fry", "vegetable stir fry"],
        "curry": ["curry", "curry dish", "indian curry"],
        "pasta sauce": ["pasta sauce", "marinara", "tomato sauce"],
        "ketchup": ["ketchup", "catsup"],
        "mustard": ["mustard", "yellow mustard", "dijon mustard"],
        "mayo": ["mayo", "mayonnaise"],
        "ranch": ["ranch", "ranch dressing"],
    }

    for item in items:
        item_lower = item.lower().strip()

        for food_name, synonyms in food_synonyms.items():
            if item_lower in synonyms:
                valid_items.append(food_name)
                break

    return valid_items
