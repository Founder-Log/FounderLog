from datetime import datetime, timedelta, timezone
import jwt
from backend.core.config import ALGORITHM, SECRET_KEY

payload = {
    "sub": "123",
    "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
}

test_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

print(test_token)