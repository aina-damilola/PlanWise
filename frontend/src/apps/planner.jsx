import "./styles/planner.css";
import React, { useState, useEffect } from "react";
import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";
import rrulePlugin from "@fullcalendar/rrule"; // Import recurrence support

function Planner() {
    const [events, setEvents] = useState([]);

    // Load predefined tasks on mount
    useEffect(() => {
        const taskData = {
            "tasks": [
                { "title": "APS 100 Exam", "start": "2024-06-25T16:00:00", "end": "2024-06-26T14:00:00" },
                { "title": "ECE 300 Study Session", "start": "2024-06-26T14:00:00" },
                { "title": "Morning Gym", "rrule": { "freq": "yearly", "dtstart": "2024-06-20T07:00:00" } },
                { "title": "Exam Prep", "start": "2024-06-28T10:00:00" }
            ]
        };
        setEvents(taskData.tasks);
    }, []);

    // Allow users to add tasks dynamically
    const handleDateClick = (info) => {
        const taskName = prompt("Enter task name:");
        if (taskName) {
            setEvents([...events, { title: taskName, start: info.dateStr }]);
        }
    };

    // Fetch schedule from Flask and update events
    async function fetchCohereSchedule() {
        const userInput = "I have an aps 100 exam on march 31st, I want to study adequately everday for this exam. I also want to go to the gym weekly and sleep everyday from 11pm to 8am";

        try {
            const response = await fetch("http://127.0.0.1:10000/generate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text: userInput })
            });
            console.log(response)
            const data = await response.json();
            console.log(data)
            const newEvents = JSON.parse(data.response).tasks; // Parse received JSON

            console.log("Received JSON from Flask:", newEvents);

            // Merge new tasks with existing events
            setEvents((prevEvents) => [...prevEvents, ...newEvents]);
        } catch (error) {
            console.error("Error fetching schedule:", error);
        }
    }

    return (
        <div>
            <h2>📅 My Task Calendar</h2>
            <button onClick={fetchCohereSchedule}>Generate Schedule</button>
            <FullCalendar
                plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin, rrulePlugin]}
                initialView="dayGridMonth"
                headerToolbar={{
                    left: "prev,next today",
                    center: "title",
                    right: "dayGridMonth,timeGridWeek,timeGridDay"
                }}
                editable={true}
                selectable={true}
                events={events} // Load JSON & recurring events
                eventContent={(arg) => (
                    <div style={{ textAlign: "center" }}>
                        <strong>{arg.event.title}</strong>
                        <br />
                        <small>{arg.timeText}</small>
                    </div>
                )}
                dateClick={handleDateClick} // Allow adding tasks
            />
        </div>
    );
}

export default Planner;
