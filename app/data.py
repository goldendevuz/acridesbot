import random

# ================= TASKS ================= #

tasks = [
    {"title": "🍔 Burger ye", "price": 3000, "desc": "Do‘sting bilan burger ye"},
    {"title": "📷 Selfie ol", "price": 5000, "desc": "3 ta odam bilan selfie"},
    {"title": "💻 VS Code och", "price": 2000, "desc": "VS Code screenshot yubor"},
    {"title": "🎧 Musiqa eshit", "price": 3000, "desc": "Musiqa eshitayotganingni ol"},
    {"title": "☕ Choy tayyorla", "price": 4000, "desc": "Choy tayyorlab video qil"},
]

# ================= HELPERS ================= #

def get_random_tasks(n=2):
    return random.sample(tasks, n)
