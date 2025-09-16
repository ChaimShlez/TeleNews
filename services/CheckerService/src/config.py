import os
from dotenv import load_dotenv

load_dotenv()
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

CATEGORIES = {
    "sexual": ["porn", "xxx", "milf", "sex", "ass", "p0rn", "s*x"],
    "drugs": ["weed", "cocaine", "marijuana", "meth", "drug", "lsd"]
}
