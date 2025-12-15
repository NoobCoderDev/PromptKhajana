import secrets
import string
from datetime import datetime, timedelta
from app import db
from app.models import OTP

OTP_EXPIRY_MINUTES = 10
MAX_OTP_ATTEMPTS = 5
OTP_LENGTH = 6

def generate_otp():
    return ''.join(secrets.choice(string.digits) for _ in range(OTP_LENGTH))

def create_otp(email, purpose):
    otp_code = generate_otp()
    expires_at = datetime.utcnow() + timedelta(minutes=OTP_EXPIRY_MINUTES)
    
    OTP.query.filter_by(email=email, purpose=purpose, is_used=False).delete()
    db.session.commit()
    
    otp_record = OTP(
        email=email,
        purpose=purpose,
        expires_at=expires_at
    )
    otp_record.set_otp(otp_code)
    
    db.session.add(otp_record)
    db.session.commit()
    
    return otp_code

def verify_otp(email, otp_code, purpose):
    otp_record = OTP.query.filter_by(
        email=email,
        purpose=purpose,
        is_used=False
    ).order_by(OTP.created_at.desc()).first()
    
    if not otp_record:
        return False, "No valid OTP found"
    
    if otp_record.is_expired():
        return False, "OTP has expired"
    
    if otp_record.attempts >= MAX_OTP_ATTEMPTS:
        return False, "Maximum verification attempts exceeded"
    
    otp_record.increment_attempts()
    
    if otp_record.check_otp(otp_code):
        otp_record.mark_as_used()
        return True, "OTP verified successfully"
    
    return False, "Invalid OTP"

def cleanup_expired_otps():
    OTP.query.filter(OTP.expires_at < datetime.utcnow()).delete()
    db.session.commit()
