import sqlite3
import json
from datetime import datetime

DB_PATH = r"C:\Users\Dominique\.local\share\mimocode\mimocode.db"
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# Get the last assistant messages from the big session (69 messages)
SESSION = "ses_08229bd02ffe4cRgsAu8ct5tLc"
print("=== LAST ASSISTANT TEXT from 'Configure mailer' session ===")
cur.execute("""
    SELECT m.time_created,
           substr(json_extract(p.data, '$.text'), 1, 2000) as text
    FROM message m
    JOIN part p ON p.message_id = m.id
    WHERE m.session_id = ?
      AND json_extract(m.data, '$.role') = 'assistant'
      AND json_extract(p.data, '$.type') = 'text'
    ORDER BY m.time_created DESC
    LIMIT 5
""", (SESSION,))
for r in cur.fetchall():
    ts = datetime.fromtimestamp(r['time_created']/1000).strftime('%H:%M:%S')
    print(f"\n[{ts}] {r['text']}")
