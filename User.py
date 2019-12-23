from psycopg2 import connect
from werkzeug.security import generate_password_hash, check_password_hash


class User:
    def __init__(self):
        self.user_id = 0
        self.user_name = None
        self.user_ip = ""
        self.user_start = ""
        self.user_kwh_price = ""
        self.user_gas_price = ""
        self.track_el = False
        self.track_g = False
        self.track_s0 = False

    @staticmethod
    def make_connection():
        conn = connect(host="localhost", database="YouLessMonitor", user="YouLessAdmin", password="admin")
        return conn

    def get(self, requested_id):
        con = self.make_connection()
        cursor = con.cursor()
        cursor.execute('SELECT id, name, ip, start, kwhprice, gasprice, track_el, track_g, track_s0'
                       ' FROM "users" where id=\'{}\''.format(ord(requested_id)))
        result = cursor.fetchone()
        if result:
            self.user_id = result[0]
            self.user_name = result[1]
            self.user_ip = result[2]
            self.user_start = result[3]
            self.user_kwh_price = result[4]
            self.user_gas_price = result[5]
            self.track_el = result[6]
            self.track_g = result[7]
            self.track_s0 = result[8]

            return self

        else:
            return None

    def register(self, username, password):
        encrypted_password = generate_password_hash(password)
        con = self.make_connection()
        cursor = con.cursor()
        cursor.execute('INSERT INTO "users" (name, password, track_s0, track_g, track_el, gasprice, kwhprice)'
                       'VALUES (\'{}\', \'{}\', False, False, False, 0, 0)'.format(username, encrypted_password))
        con.commit()

    def validate_login(self, username, password):
        con = self.make_connection()
        cursor = con.cursor()
        cursor.execute('SELECT password, id FROM "users" WHERE name=\'{}\''.format(username))
        result = cursor.fetchone()
        if result:
            temp_pw = result[0]
            success = check_password_hash(temp_pw, password)
            if success:
                user_id = result[1]
                return self.get(chr(user_id))
            else:
                return None
        return None

    def update_settings(self, ip, start_date, enable_el, enable_g, enable_s0, kwhprice, gasprice):
        operation = 'UPDATE "Users" SET '

        if ip != "":
            operation += "ip = '{}', ".format(ip)

        if start_date != "":
            temp = start_date.split('/')
            start_date = temp[1] + "/" + temp[0] + "/" + temp[2]
            operation += "start = '{}', ".format(start_date)

        if enable_el == "on":
            operation += "track_el = true, "
        else:
            operation += "track_el = false, "

        if enable_g == "on":
            operation += "track_g = true, "
        else:
            operation += "track_g = false, "

        if enable_s0 == "on":
            operation += "track_s0 = true, "
        else:
            operation += "track_s0 = false, "

        if kwhprice != "":
            operation += "kwhprice = '{}', ".format(kwhprice)

        if gasprice != "":
            operation += "gasprice = '{}', ".format(gasprice)

        operation = operation[:-2] + " WHERE name='{}'".format(self.user_name)
        con = self.make_connection()
        cursor = con.cursor()
        cursor.execute(operation)
        con.commit()

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return chr(self.user_id)
