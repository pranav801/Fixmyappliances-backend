from django.core.mail import send_mail


def send_employee_status_email(user_email, first_name, action,temp_password):
    subject1 = "Your request got accepted"
    subject2 = "Your request got rejected"

    if action==True:
        message = f"""
        <html>
        <body style="background-color: #f5f5f5; font-family: Arial, sans-serif; padding: 20px;">
            <div style="background-color: #ffffff; padding: 20px; border-radius: 5px; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);">
                <h1 style="color: #333333;">Subject: {subject1}</h1>
                <p>Hello {first_name},</p>
                <p>We glad to inform you that your account has been approved.</p>
                </br>
                <p>User Name : {user_email}</p>
                <p>Password : {temp_password}</p>
                </br>
                <p>Here we given the Username and password to login, You can change the password as your wish </p>
                <p>If you believe this is an error or have any questions regarding your account status, please contact our support team at fixmyappliances.kerala@gmail.com.</p>
                
                <p>Thank you for your understanding.</p>
                
                <p>Best regards,<br>fixmyappliances.kerala@gmail.com</p>
            </div>
        </body>
        </html>
        """.format(
            subject=subject1, username=first_name
        )

        send_mail(
            subject1, "", "fixmyappliances.kerala@gmail.com", [user_email], html_message=message
        )
    elif action==False:
        message = f"""
        <html>
        <body style="background-color: #f5f5f5; font-family: Arial, sans-serif; padding: 20px;">
            <div style="background-color: #ffffff; padding: 20px; border-radius: 5px; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);">
                <h1 style="color: #333333;">Subject: {subject2}</h1>
                <p>Hello {first_name},</p>
                <p>We regret to inform you that your account has been suspended.</p>
                
                <p>If you believe this is an error or have any questions regarding your account status, please contact our support team at fixmyappliances.kerala@gmail.com.</p>
                
                <p>Thank you for your understanding.</p>
                
                <p>Best regards,<br>fixmyappliances.kerala@gmail.com</p>
            </div>
        </body>
        </html>
        """.format(
            subject=subject2, username=first_name
        )

        send_mail(
            subject2, "", "fixmyappliances.kerala@gmail.com", [user_email], html_message=message
        )