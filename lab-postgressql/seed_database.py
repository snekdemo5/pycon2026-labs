import json
import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv


load_dotenv()


def get_connection():
    return psycopg.connect(
        host=os.environ["POSTGRES_HOST"],
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        port=os.environ.get("POSTGRES_PORT", "5432"),
        sslmode="require",
    )


def main():
    notes_path = Path(__file__).resolve().parent / "data" / "notes.json"

    with notes_path.open("r", encoding="utf-8") as file:
        notes = json.load(file)

    with get_connection() as conn:
        with conn.cursor() as cur:
            for note in notes:
                cur.execute(
                    """
                    INSERT INTO notes (title, content)
                    VALUES (%s, %s)
                    """,
                    (note["title"], note["content"]),
                )

        conn.commit()

    print(f"Inserted {len(notes)} notes.")


if __name__ == "__main__":
    main()