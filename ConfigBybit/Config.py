# How to get Bybit API Token:
# 1. Register your account at Bybit https://www.bybit.com/invite?ref=KXLXXE%230
# 2. Go to "Profile" -> "API Management" https://www.bybit.com/app/user/api-management?ref=KXLXXE%230
# 3. Then push the button "Create New Key" and select "System generated"
# 4. In "API Key restrictions" enable "Read-Write" and in "Unified Trading"->"SPOT" enable "Trade"
# 5. Copy & Paste here "API Key" and "Secret Key"
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# P.S. If you use my referral link - Thanks a lot))
# If you liked this software => Put a star on github - https://github.com/WISEPLAT/backtrader_bybit
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


class Config:
    BYBIT_API_KEY = "YOUR_API_KEY"
    BYBIT_API_SECRET = "YOUR_SECRET_KEY"
    BYBIT_ACCOUNT_TYPE = "UNIFIED"  # UNIFIED or CONTRACT
