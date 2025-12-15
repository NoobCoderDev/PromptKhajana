from flask_mail import Message
from flask import current_app

def get_mail():
    from app import mail
    return mail

def send_otp_email(email, otp_code, purpose):
    mail = get_mail()
    
    subject_map = {
        'signup': 'Verify Your Email - Prompt Khajana',
        'login': 'Login Verification Code - Prompt Khajana',
        'reset': 'Password Reset Code - Prompt Khajana'
    }
    
    purpose_text_map = {
        'signup': 'complete your registration',
        'login': 'log in to your account',
        'reset': 'reset your password'
    }
    
    subject = subject_map.get(purpose, 'Verification Code - Prompt Khajana')
    purpose_text = purpose_text_map.get(purpose, 'verify your request')
    
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }}
            .container {{
                max-width: 600px;
                margin: 40px auto;
                background-color: #ffffff;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                overflow: hidden;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 28px;
            }}
            .content {{
                padding: 40px 30px;
            }}
            .otp-box {{
                background-color: #f8f9fa;
                border: 2px dashed #667eea;
                border-radius: 8px;
                padding: 20px;
                text-align: center;
                margin: 30px 0;
            }}
            .otp-code {{
                font-size: 36px;
                font-weight: bold;
                color: #667eea;
                letter-spacing: 8px;
                font-family: 'Courier New', monospace;
            }}
            .warning {{
                background-color: #fff3cd;
                border-left: 4px solid #ffc107;
                padding: 15px;
                margin: 20px 0;
                border-radius: 4px;
            }}
            .footer {{
                background-color: #f8f9fa;
                padding: 20px;
                text-align: center;
                color: #6c757d;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔐 Prompt Khajana</h1>
            </div>
            <div class="content">
                <h2>Email Verification Code</h2>
                <p>Hello,</p>
                <p>You requested to {purpose_text}. Please use the following One-Time Password (OTP) to proceed:</p>
                
                <div class="otp-box">
                    <div class="otp-code">{otp_code}</div>
                </div>
                
                <p><strong>This code will expire in 10 minutes.</strong></p>
                
                <div class="warning">
                    <strong>⚠️ Security Notice:</strong>
                    <ul style="margin: 10px 0; padding-left: 20px;">
                        <li>Never share this code with anyone</li>
                        <li>Our team will never ask for your OTP</li>
                        <li>If you didn't request this, please ignore this email</li>
                    </ul>
                </div>
                
                <p>If you have any questions, please contact our support team.</p>
                <p>Best regards,<br><strong>Prompt Khajana Team</strong></p>
            </div>
            <div class="footer">
                <p>This is an automated message, please do not reply to this email.</p>
                <p>&copy; 2024 Prompt Khajana. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    text_body = f"""
    Prompt Khajana - Email Verification
    
    Hello,
    
    You requested to {purpose_text}. Please use the following One-Time Password (OTP):
    
    {otp_code}
    
    This code will expire in 10 minutes.
    
    Security Notice:
    - Never share this code with anyone
    - Our team will never ask for your OTP
    - If you didn't request this, please ignore this email
    
    Best regards,
    Prompt Khajana Team
    """
    
    try:
        msg = Message(
            subject=subject,
            recipients=[email],
            html=html_body,
            body=text_body
        )
        mail.send(msg)
        return True
    except Exception as e:
        current_app.logger.error(f"Failed to send email: {str(e)}")
        return False
