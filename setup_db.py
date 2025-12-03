import getpass
import argparse
import secrets
import string
import sys

import mysql.connector
from mysql.connector import Error

DB_NAME = "budget_tracker"
APP_USER = "budget_user"

USERS_SQL = """
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(190) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL
);
"""

CATEGORIES_SQL = """
CREATE TABLE IF NOT EXISTS categories (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  name VARCHAR(100) NOT NULL,
  color CHAR(7) DEFAULT '#999999',
  UNIQUE KEY uniq_user_name (user_id, name),
  CONSTRAINT fk_cat_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
"""

TRANSACTIONS_SQL = """
CREATE TABLE IF NOT EXISTS transactions (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  amount DECIMAL(12,2) NOT NULL,
  type ENUM('income','expense') NOT NULL,
  description VARCHAR(255),
  date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  category_id INT NULL,
  CONSTRAINT fk_tx_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  CONSTRAINT fk_tx_cat  FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
);
"""

def gen_password(length: int = 22) -> str:
    # gut für Copy&Paste, vermeidet Leerzeichen/Anführungszeichen
    alphabet = string.ascii_letters + string.digits + "-._@#%+="
    return "".join(secrets.choice(alphabet) for _ in range(length))

def main() -> int:
    ap = argparse.ArgumentParser(description="Einmaliges Setup für MySQL DB budget_tracker")
    ap.add_argument("--host", default="localhost")
    ap.add_argument("--port", default=3306, type=int)
    ap.add_argument("--root-user", default="root")
    args = ap.parse_args()

    root_pass = getpass.getpass("MySQL root password: ")

    try:
        conn = mysql.connector.connect(
            host=args.host, port=args.port, user=args.root_user, password=root_pass, autocommit=True
        )
    except Error as e:
        print(f"[ERROR] Root-Login fehlgeschlagen: {e}")
        return 2

    try:
        cur = conn.cursor()

        # DB anlegen
        cur.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;")
        cur.execute(f"USE {DB_NAME};")

        # Tabellen anlegen
        cur.execute(USERS_SQL)
        cur.execute(CATEGORIES_SQL)
        cur.execute(TRANSACTIONS_SQL)

        # App-User anlegen + Rechte
        app_pass = gen_password()
        cur.execute(f"CREATE USER IF NOT EXISTS '{APP_USER}'@'localhost' IDENTIFIED BY %s;", (app_pass,))
        cur.execute(f"GRANT ALL PRIVILEGES ON {DB_NAME}.* TO '{APP_USER}'@'localhost';")
        cur.execute("FLUSH PRIVILEGES;")

        print("\n✅ Fertig.")
        print(f"Database .........: {DB_NAME}")
        print(f"App User .........: {APP_USER}@localhost")
        print(f"App Password .....: {app_pass}\n")
        print("Bitte Passwort sicher speichern und in deiner App-Konfiguration verwenden.")
        return 0
    except Error as e:
        print(f"[ERROR] SQL-Fehler: {e}")
        return 3
    finally:
        try:
            cur.close()
            conn.close()
        except Exception:
            pass

if __name__ == "__main__":
    sys.exit(main())