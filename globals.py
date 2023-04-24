import os 

APP_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_FOLDER = os.path.join(APP_ROOT, "uploads")
SECRET_KEY = "many random bytes"    

CATEGORIES = [
    ("Cooking", "Cooking"),
    ("Dance", "Dance"),
    ("Art", "Art"),
    ("Gaming", "Gaming"),
    ("Sports", "Sports"),
    ("STEM", "STEM"),
    ("Music", "Music"),
    ("Travel", "Travel"),
    ("Health", "Health"),
    ("Education", "Education"),
    ("Entertainment", "Entertainment"),
]