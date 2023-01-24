import React, { useState, useEffect } from 'react';
import BigCalendar from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import ical from 'ical.js';

const Calendar = ({ url }) => {
    const [events, setEvents] = useState([]);

    useEffect(() => {
        fetch(url)
            .then(res => res.text())
            .then(data => {
                const jCalData = ical.parse(data);
                const comp = new ical.Component(jCalData);
                const eventList = comp.getAllSubcomponents('vevent');
                const events = eventList.map(event => {
                    const start = event.getFirstPropertyValue('dtstart').toJSDate();
                    const end = event.getFirstPropertyValue('dtend').toJSDate();
                    const summary = event.getFirstPropertyValue('summary');
                    return { start, end, title: summary };
                });
                setEvents(events);
            })
            .catch(err => console.log(err));
    }, [url]);

    return (
        <div>
            <BigCalendar
                events={events}
                startAccessor="start"
                endAccessor="end"
                defaultView="month"
            />
        </div>
    );
}

export default Calendar
