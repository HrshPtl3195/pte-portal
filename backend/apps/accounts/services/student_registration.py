from django.db import connection

def register_student(
    email, password_hash, first_name, middle_name, last_name, phone, gender, birth_date, timezone='UTC', locale='en'
):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT accounts.register_student(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, [email, password_hash, first_name, middle_name, last_name, phone, gender, birth_date, timezone, locale])
        user_id = cursor.fetchone()[0]
    return user_id
