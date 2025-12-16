import React, { useState, useEffect, useCallback } from 'react';


const generateTimeSlots = (reservedSlots) => {
    const slots = [];
    const START_TIME_MINUTES = 8 * 60; // 8:00 AM
    const END_TIME_MINUTES = 15 * 60 + 30; // 3:30 PM (15:30)

    for (let currentMinutes = START_TIME_MINUTES; currentMinutes <= END_TIME_MINUTES; currentMinutes += 30) {
        const hours = Math.floor(currentMinutes / 60);
        const minutes = currentMinutes % 60;
        const timeString = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}`;
        const isReserved = reservedSlots.some(slot => slot.time === timeString && slot.is_reserved === 1);
        
        slots.push({
            time: timeString,
            isReserved: isReserved,
        });
    }
    return slots;
};

const formatDate = (date) => {
    const d = new Date(date);
    let month = '' + (d.getMonth() + 1);
    let day = '' + d.getDate();
    const year = d.getFullYear();

    if (month.length < 2) month = '0' + month;
    if (day.length < 2) day = '0' + day;

    return [year, month, day].join('-');
};


const SlotPicker = () => {
    const [selectedDate, setSelectedDate] = useState(formatDate(new Date()));
    const [slots, setSlots] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const fetchSlots = useCallback(async (date) => {
        setLoading(true);
        setError(null);
        try {
            const response = await fetch(`http://localhost:5000/api/slots/${date}`);
            if (!response.ok) throw new Error('Failed to fetch slots.');
            const reservedData = await response.json(); 
            const fullSlotsList = generateTimeSlots(reservedData);
            setSlots(fullSlotsList);
            
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }, []); // generateTimeSlots is outside, no need to include in dependency array

    useEffect(() => {
        // Fetch slots whenever the selected date changes
        fetchSlots(selectedDate);
    }, [selectedDate, fetchSlots]);


    // --- Handle Reservation ---
    const handleReserve = async (time) => {
        if (!window.confirm(`Are you sure you want to reserve the slot on ${selectedDate} at ${time}?`)) {
            return;
        }

        try {
            const response = await fetch('http://localhost:5000/api/reserve', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ date: selectedDate, time }),
            });

            if (!response.ok) {
                // If the server returns a 409 (Conflict), handle it
                const errorData = await response.json();
                throw new Error(errorData.message || 'Reservation failed.');
            }

            // Success: Re-fetch the slots to update the UI
            alert(`Slot ${time} reserved successfully!`);
            fetchSlots(selectedDate);

        } catch (err) {
            alert(`Reservation Error: ${err.message}`);
        }
    };
    
    // --- Handle Reservation ---
    const freeReserve = async (time) => {
        if (!window.confirm(`Are you sure you want to free the slot on ${selectedDate} at ${time}?`)) {
            return;
        }

        try {
            const response = await fetch('http://localhost:5000/api/unreserve', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ date: selectedDate, time }),
            });

            if (!response.ok) {
                // If the server returns a 409 (Conflict), handle it
                const errorData = await response.json();
                throw new Error(errorData.message || 'Free failed.');
            }

            // Success: Re-fetch the slots to update the UI
            alert(`Slot ${time} freed successfully!`);
            fetchSlots(selectedDate);

        } catch (err) {
            alert(`Free Error: ${err.message}`);
        }
    };
    

    return (
        <div>
            <h2>🗓 Slot Reservation</h2>

            {/* Date Picker */}
            <input 
                type="date" 
                value={selectedDate} 
                onChange={(e) => setSelectedDate(e.target.value)} 
                style={{ padding: '10px', marginBottom: '20px', fontSize: '16px' }}
            />

            {error && <p style={{ color: 'red' }}>Error: {error}</p>}
            {loading ? (
                <p>Loading slots...</p>
            ) : (
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(100px, 1fr))', gap: '10px' }}>
                    {slots.map((slot) => (
                        <div>
                        <button
                            key={slot.time}
                            onClick={() => {handleReserve(slot.time)}}
                            disabled={slot.isReserved}
                            style={{
                                padding: '10px 5px',
                                fontSize: '14px',
                                cursor: slot.isReserved ? 'not-allowed' : 'pointer',
                                backgroundColor: slot.isReserved ? '#ff6b6b' : '#4CAF50',
                                color: 'white',
                                border: 'none',
                                borderRadius: '5px'
                            }}
                        >
                            {slot.time} {slot.isReserved && '(Reserved)'}
                        </button>
                        <button
                            key={slot.time}
                            onClick={() => {freeReserve(slot.time)}}
                            disabled={!slot.isReserved}
                            style={{
                                padding: '10px 5px',
                                fontSize: '14px',
                                cursor: !slot.isReserved ? 'not-allowed' : 'pointer',
                                backgroundColor: !slot.isReserved ? '#ff6b6b' : '#4CAF50',
                                color: 'white',
                                border: 'none',
                                borderRadius: '5px'
                            }}
                        >
                            FREE SLOT
                        </button>
                        </div>
                    ))}
                    {slots.length === 0 && selectedDate && <p>No slots available for this date.</p>}
                </div>
            )}
        </div>
    );
};

export default SlotPicker;
