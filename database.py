import aiosqlite
import config

async def init_db() -> None:
    """Initialize SQLite database and schema."""
    async with aiosqlite.connect(config.DB_PATH) as db:
        await db.execute("PRAGMA journal_mode=WAL")
        await db.execute('''
            CREATE TABLE IF NOT EXISTS BUTTON_CACHE (
                msg_key TEXT PRIMARY KEY,
                text TEXT NOT NULL,
                TIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS BOT_STATS (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_type TEXT NOT NULL,
                duration INTEGER NOT NULL,
                username TEXT NOT NULL,
                file_size REAL NOT NULL,
                processing_time REAL NOT NULL,
                TIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.commit()

async def save_transcription(msg_key: str, text: str) -> None:
    """Save transcription text to cache."""
    async with aiosqlite.connect(config.DB_PATH) as db:
        await db.execute(
            "INSERT OR REPLACE INTO BUTTON_CACHE (msg_key, text) VALUES (?, ?)",
            (msg_key, text)
        )
        await db.commit()

async def save_stats(
    file_type: str, 
    duration: int, 
    username: str, 
    file_size: float, 
    processing_time: float
) -> None:
    """Log performance metrics and metadata."""
    async with aiosqlite.connect(config.DB_PATH) as db:
        await db.execute('''
            INSERT INTO BOT_STATS (file_type, duration, username, file_size, processing_time)
            VALUES (?, ?, ?, ?, ?)
        ''', (file_type, duration, username, file_size, processing_time))
        await db.commit()

async def get_transcription(msg_key: str) -> str | None:
    """Retrieve transcription text by message key."""
    async with aiosqlite.connect(config.DB_PATH) as db:
        async with db.execute("SELECT text FROM BUTTON_CACHE WHERE msg_key = ?", (msg_key,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None