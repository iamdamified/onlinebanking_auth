import random, time

otp_store = {}

def generate_otp(email):
    otp = str(random.randint(100000, 999999))
    otp_store[email] = {"otp": otp, "expires": time.time() + 300}
    return otp

def verify_otp(email, otp):
    record = otp_store.get(email)
    if not record:
        return False
    if time.time() > record["expires"]:
        return False
    return record["otp"] == otp