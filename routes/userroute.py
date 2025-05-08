
import time
import traceback

from fastapi import APIRouter, HTTPException, Response, Request
import jwt

from database import usersdb
from models.usermodel import User, User2

SECRET_KEY = "your_secret_key"  # ✅ Replace with a strong secret key
router = APIRouter()




@router.post("/login")
async def user_login( user: User, response:Response):
    try:
        # ✅ Validate user credentials
        findusertype = await usersdb.find_one(
            {"userID": user.userID, "user_passwd": user.user_passwd},
            {"_id": 0, "user_type": 1}
        )

        if not findusertype:
            raise HTTPException(status_code=401, detail="Invalid Credentials")



        # ✅ Generate JWT token after authentication
        token_payload = {
            "user_id": user.userID,
            "user_type": findusertype["user_type"],
            "exp": int(time.time()) + (2*60*60) # ✅ Corrected timedelta usage
        }
        token = jwt.encode(token_payload, SECRET_KEY, algorithm="HS256")

        # ✅ Securely store token in HttpOnly cookies
        response.set_cookie(
            key="auth_token",
            value=token,
            httponly=True,
            secure=True,
            samesite="none"
        )

        return {"status": "success", "user_type": findusertype["user_type"], "token": token}

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

@router.post("/logout")
async def user_logout(response: Response):
    try:
        # ✅ Remove the authentication token from cookies
        response.delete_cookie("auth_token")

        return {"status": "success", "message": "User logged out successfully!"}

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Logout failed: {str(e)}")