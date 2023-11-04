from django.core.mail import send_mail

def send_complaint_status_email(user_email, first_name, status, booking_id):
    subject = "Complaint Status Update"
    message = ""

    if status == "pending":
        subject = "Complaint Pending"
        message = f"""
        <html>
        <body style="background-color: #f5f5f5; font-family: Arial, sans-serif; padding: 20px;">
            <div style="background-color: #ffffff; padding: 20px; border-radius: 5px; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);">
                <h1 style="color: #333333;">Subject: {subject}</h1>
                <p>Hello {first_name},</p>
                <p>Your complaint with (BookingId: {booking_id}) is currently pending. We have received your complaint and are working on it.</p>
                <p>Thank you for your patience. We will update you as soon as the issue is resolved.</p>
                <p>If you have any questions or need further assistance, please contact our support team at fixmyappliances.kerala@gmail.com.</p>
                <p>Best regards,<br>fixmyappliances.kerala@gmail.com</p>
            </div>
        </body>
        </html>
        """.format(
            subject=subject, username=first_name
        )
    elif status == "resolved":
        subject = "Complaint Resolved"
        message = f"""
        <html>
        <body style="background-color: #f5f5f5; font-family: Arial, sans-serif; padding: 20px;">
            <div style="background-color: #ffffff; padding: 20px; border-radius: 5px; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);">
                <h1 style="color: #333333;">Subject: {subject}</h1>
                <p>Hello {first_name},</p>
                <p>Your complaint with (BookingId: {booking_id}) has been resolved. We have successfully addressed the issue you reported.</p>
                <p>If you have any further questions or need additional assistance, please don't hesitate to contact our support team at fixmyappliances.kerala@gmail.com.</p>
                <p>Best regards,<br>fixmyappliances.kerala@gmail.com</p>
            </div>
        </body>
        </html>
        """.format(
            subject=subject, username=first_name
        )
    elif status == "solved":
        subject = "Complaint Solved"
        message = f"""
        <html>
        <body style="background-color: #f5f5f5; font-family: Arial, sans-serif; padding: 20px;">
            <div style="background-color: #ffffff; padding: 20px; border-radius: 5px; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);">
                <h1 style="color: #333333;">Subject: {subject}</h1>
                <p>Hello {first_name},</p>
                <p>We are pleased to inform you that your complaint with (BookingId: {booking_id}) has been solved to your satisfaction.</p>
                <p>If you have any more concerns or require further assistance, please reach out to our support team at fixmyappliances.kerala@gmail.com.</p>
                <p>Best regards,<br>fixmyappliances.kerala@gmail.com</p>
            </div>
        </body>
        </html>
        """.format(
            subject=subject, username=first_name
        )

    if message:
        send_mail(
            subject, "", "fixmyappliances.kerala@gmail.com", [user_email], html_message=message
        )
