const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const cors = require('cors'); // To allow React (localhost:3000) to talk to the server (localhost:5000)

const app = express();
const PORT = 5000;

// Middleware
app.use(cors());
app.use(express.json());

// Initialize SQLite Database
const db = new sqlite3.Database('./slots.db', (err) => {
  if (err) {
    console.error('Database connection error:', err.message);
  } else {
    console.log('Connected to the SQLite database.');
    // Create the table if it doesn't exist
    db.run(`CREATE TABLE IF NOT EXISTS slots (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      date TEXT NOT NULL,
      time TEXT NOT NULL,
      is_reserved INTEGER DEFAULT 0
    )`);
  }
});

// --- API Endpoints ---

// 1. Get available slots for a specific date
app.get('/api/slots/:date', (req, res) => {
  const { date } = req.params;
  // Get all slots for that date (reserved or not)
  db.all('SELECT * FROM slots WHERE date = ? ORDER BY time', [date], (err, rows) => {
    if (err) {
      res.status(500).json({ error: err.message });
      return;
    }
    // Generate all possible slots and merge with reserved ones (See Step 2)
    // For simplicity here, we only return the reserved ones.
    // **In a real app, you'd generate the full list on the server and mark the reserved ones.**

    // --- CONCEPT: Generate all slots ---
    const allSlots = [];
    const startTime = 8 * 60; // 8:00 AM in minutes
    const endTime = 15 * 60 + 30; // 3:30 PM in minutes (3:00 PM is 15:00)

    for (let currentMinutes = startTime; currentMinutes <= endTime; currentMinutes += 30) {
        const hours = Math.floor(currentMinutes / 60);
        const minutes = currentMinutes % 60;
        const time = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}`;
        
        // Find if this time slot is in the reserved rows
        const reservedSlot = rows.find(row => row.time === time);

        allSlots.push({
            id: reservedSlot ? reservedSlot.id : null,
            date: date,
            time: time,
            is_reserved: reservedSlot ? reservedSlot.is_reserved : 0,
        });
    }

    res.json(allSlots);
  });
});

// 2. Reserve a slot
app.post('/api/reserve', (req, res) => {
  const { date, time } = req.body;

  // Check if the slot is already reserved (optional, but good practice)
  db.get('SELECT * FROM slots WHERE date = ? AND time = ?', [date, time], (err, row) => {
   if (err) {
      res.status(500).json({ error: err.message });
      return;
    }

    if (row && row.is_reserved === 1) {
      // Slot is already reserved (update the row)
      res.status(409).json({ message: 'Slot is already reserved.' });
      return;
    }

    // Insert or Update the slot to be reserved
    // UPSERT logic: If the slot exists, update it, otherwise insert it.
    // For simplicity, we assume we only care about reserved slots in the DB.
    db.run(
      'INSERT INTO slots (date, time, is_reserved) VALUES (?, ?, 1)',
      [date, time],
      function (err) {
        if (err) {
          res.status(500).json({ error: err.message });
          return;
        }
        res.status(201).json({ 
          message: 'Slot reserved successfully',
          id: this.lastID,
          date,
          time
        });
      }
    );
  });
});

// 3. Unreserve a slot
app.post('/api/unreserve', (req, res) => {
  const { date, time } = req.body;

  // 1. Check if the slot exists and is currently reserved
  db.get(
    'SELECT * FROM slots WHERE date = ? AND time = ?',
    [date, time],
    (err, row) => {
      if (err) {
        res.status(500).json({ error: err.message });
        return;
      }

      // If the row doesn't exist or is not reserved (assuming 0 is unreserved)
      if (!row || row.is_reserved !== 1) {
        res.status(404).json({ message: 'Slot is not currently reserved or does not exist.' });
        return;
      }

      // 2. Unreserve the slot by setting is_reserved to 0
      db.run(
        'UPDATE slots SET is_reserved = 0 WHERE date = ? AND time = ?',
        [date, time],
        function (err) {
          if (err) {
            res.status(500).json({ error: err.message });
            return;
          }

          // Check if any rows were actually changed (should be 1)
          if (this.changes === 0) {
            res.status(500).json({ error: 'Failed to unreserve slot.' });
            return;
          }

          res.status(200).json({
            message: 'Slot unreserved successfully',
            date,
            time,
          });
        }
      );
    }
  );
});


app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
