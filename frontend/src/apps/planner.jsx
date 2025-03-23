import "./styles/planner.css";
import React, { useState, useEffect } from "react";
import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";
import rrulePlugin from "@fullcalendar/rrule"; // Import recurrence support

function Planner() {
    const [events, setEvents] = useState([]);
    const [userMessage, setUserMessage] = useState("");



    // Allow users to add tasks dynamically
    const handleDateClick = (info) => {
        const taskName = prompt("Enter task name:");
        if (taskName) {
            setEvents((prevEvents) => [
                ...prevEvents,
                { title: taskName, start: info.dateStr }
            ]);
        }
    };

    // Fetch schedule from Flask and update events
    async function fetchCohereSchedule() {
        const userInput = userMessage;

        try {
            const response = await fetch("http://127.0.0.1:10000/generate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text: userInput })
            });
            const data = await response.json();
            const newEvents = JSON.parse(data.response).tasks; // Parse received JSON

            console.log("Received JSON from Flask:", newEvents);

            // Merge new tasks with existing events
            setEvents((prevEvents) => [...prevEvents, ...newEvents]);
        } catch (error) {
            console.error("Error fetching schedule:", error);
        }
    }

    return (
        <div id="planner">
            <h2 className="inter">Dynamic Calendar</h2>

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
            <div id="actions">
                <input 
                    type="text" 
                    placeholder="Enter your message" 
                    value={userMessage} 
                    onChange={(e) => setUserMessage(e.target.value)} 
                    className="inter"
                />
                <button onClick={fetchCohereSchedule}/>
            </div>
            
        </div>
    );
}

export default Planner;
