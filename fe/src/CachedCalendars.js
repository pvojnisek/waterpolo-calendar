import React, { useState, useEffect } from 'react';
import './cachedCalendars.css'

function CachedCalendars() {
    const [data, setData] = useState([]);
    const [inputUrl, setInputUrl] = useState('');
    const [content, setCalendarContent] = useState('');

    useEffect(() => {
        fetch('http://localhost:8000/waterpolo/cached_calendars')
            .then(res => res.json())
            .then(data => setData(data))
            .catch(err => console.log(err));
    }, []);

    const handleClick = (item) => {
        const url = `http://localhost:8000/waterpolo/${item.tournament}/${item.team}`;
        setInputUrl(url);
    }

    const handleLoadCalendar = () => {
        fetch(inputUrl)
            .then(res => res.text())
            .then(text => setCalendarContent(text))
            .catch(err => console.log(err));
    }

    return (
        <div className='cachedCalendars'>
            <h2>Cached Calendars</h2>
            <p> Number of items: {data.length} </p>
            <ul>
                {data.map((item, index) => (
                    <li key={index} onClick={() => handleClick(item)}>
                        Tournament: {item.tournament}, Team: {item.team}, Size: {item.size}
                    </li>
                ))}
            </ul>
            <button className="calendar-button" type='button' onClick={handleLoadCalendar} >Load calendar</button>
            <input className="calendar-url" type="text" value={inputUrl} readOnly />
            <hr></hr>
            <textarea
                className="calendar-content"
                value={content}
                rows={20}
                readOnly={true}
            ></textarea>
        </div>
    );
}

export default CachedCalendars;
