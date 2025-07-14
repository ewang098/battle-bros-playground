import os
import asyncio
import argparse

from databases import Database

DATABASE_URL = os.getenv("DATABASE_URL")

SQL_CMDS = [
    # Create enum types if not exists
    """
    DO $$
    BEGIN
      IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'bro_type') THEN
        CREATE TYPE bro_type AS ENUM ('build', 'real');
      END IF;
      IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'stars_enum') THEN
        CREATE TYPE stars_enum AS ENUM ('0', '1', '2', '3');
      END IF;
    END$$;
    """,

    # Create table with final column nullability
    """
    CREATE TABLE IF NOT EXISTS BattleBros (
      id SERIAL PRIMARY KEY,
      name VARCHAR(100) UNIQUE NOT NULL,
      type bro_type NOT NULL,

      fatigue INTEGER,
      fatigueStars stars_enum,

      hp INTEGER,
      hpStars stars_enum,

      resolve INTEGER,
      resolveStars stars_enum,

      meleeAtk INTEGER,
      meleeAtkStars stars_enum,

      meleeDef INTEGER,
      meleeDefStars stars_enum,

      initiative INTEGER,
      initiativeStars stars_enum,

      rangeAtk INTEGER,
      rangeAtkStars stars_enum,

      rangeDef INTEGER,
      rangeDefStars stars_enum
    );
    """,

    # Insert seed data
    """
    INSERT INTO BattleBros (
      name, type, fatigue, fatigueStars, hp, hpStars, resolve, resolveStars,
      meleeAtk, meleeAtkStars, meleeDef, meleeDefStars,
      initiative, initiativeStars, rangeAtk, rangeAtkStars, rangeDef, rangeDefStars
    ) VALUES
      ('BF_Tank', 'build', 115, '0', NULL, NULL, NULL, NULL, NULL, NULL, 35, '0', NULL, NULL, NULL, NULL, NULL, NULL),
      ('Nimble_Tank', 'build', NULL, NULL, 90, '0', NULL, NULL, NULL, NULL, 35, '0', NULL, NULL, NULL, NULL, NULL, NULL),
      ('Fodder_Tank', 'build', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 35, '0', NULL, NULL, NULL, NULL, NULL, NULL),
      ('Nimble_Duelist', 'build', NULL, NULL, 90, '0', NULL, NULL, 85, '0', 35, '0', NULL, NULL, NULL, NULL, NULL, NULL),
      ('Nimble_2H_Sword', 'build', NULL, NULL, 90, '0', NULL, NULL, 85, '0', 35, '0', NULL, NULL, NULL, NULL, NULL, NULL)
    ON CONFLICT (name) DO NOTHING;
    """
]

async def apply_sql(dry_run=False):
    if dry_run:
        print("DRY RUN: SQL statements to be executed:")
        for i, cmd in enumerate(SQL_CMDS, 1):
            print(f"\n--- Statement {i} ---\n{cmd.strip()}")
        return

    database = Database(DATABASE_URL)
    await database.connect()

    for i, cmd in enumerate(SQL_CMDS, 1):
        print(f"Executing SQL statement {i}...")
        await database.execute(cmd)

    await database.disconnect()
    print("✅ Database initialized successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Initialize the BattleBros database.")
    parser.add_argument('--dry-run', action='store_true', help="Print SQL statements without executing them.")
    args = parser.parse_args()

    asyncio.run(apply_sql(dry_run=args.dry_run))
