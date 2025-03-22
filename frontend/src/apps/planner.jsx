import "./styles/planner.css"
import { useState, useEffect } from "react";
//I have APS 100 and ECE 300 and want to study efficiently for those courses, I also want to not forget about my exam on friday at 6:30pm - 8pm.
//Give me an empty schedule
//WwNgPjpfa2Btwiv0pKw7jJzXTGLoAKbgLnaVs04l
function Planner() {
    const [currentDate, setCurrentDate] = useState(new Date());

    const [events, setEvents] = useState({});
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function fetchCohereSchedule() {
            const API_KEY = "WwNgPjpfa2Btwiv0pKw7jJzXTGLoAKbgLnaVs04l";  // Replace this
            const API_URL = "https://api.cohere.ai/v1/generate";

            const requestData = {
                model: "command",
                prompt: 'I have an APS 100 exam on Wednesday at 4pm to 6pm and an ECE 300 exam from Friday at 7pm to 9pm. I want to study for these courses prior to the exam. I also want to have a gym session every morning each day. Generate a JSON object representing a weekly schedule. Format it as follows: {"schedule": [{"day": "Sunday","events": [{"name": "Event Name","time": "HH:MM AM/PM - HH:MM AM/PM"}]},{"day": "Monday","events": [{"name": "Event Name","time": "HH:MM AM/PM - HH:MM AM/PM"}]},{"day": "Tuesday","events": [{"name": "Event Name","time": "HH:MM AM/PM - HH:MM AM/PM"}]},{"day": "Wednesday","events": [{"name": "Event Name","time": "HH:MM AM/PM - HH:MM AM/PM"}]},{"day": "Thursday","events": [{"name": "Event Name","time": "HH:MM AM/PM - HH:MM AM/PM"}]},{"day": "Friday","events": [{"name": "Event Name","time": "HH:MM AM/PM - HH:MM AM/PM"}]},{"day": "Saturday","events": [{"name": "Event Name","time": "HH:MM AM/PM - HH:MM AM/PM"}]}]}. Do not include any additional text before or after.',
                max_tokens: 1000,
                temperature: 0.5
            };

            try {
                const response = await fetch(API_URL, {
                    method: "POST",
                    headers: {
                        "Authorization": `Bearer ${API_KEY}`,
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(requestData)
                });

                const data = await response.json();
                
                const rawText = data.generations[0].text;
                console.log(rawText)
                try {
                    const jsonStart = rawText.indexOf("{");
                    const jsonEnd = rawText.lastIndexOf("}") + 1;
                    let validJson = rawText.slice(jsonStart, jsonEnd);
                    const parsedSchedule = JSON.parse(validJson);
                    setEvents(parsedSchedule);
                    console.log(parsedSchedule); 
                } catch (error) {
                    console.error("Invalid JSON:", error.message);
                }
            
                setLoading(false);
            } catch (err) {
                setError("Failed to fetch schedule from Cohere");
                setLoading(false);
            }
        }

        fetchCohereSchedule();
    }, []);

    if (loading) return <p>Loading schedule...</p>;
    if (error) return <p>{error}</p>;

   {/* const [events, setEvents] = useState({
        "schedule": [
            {
                "day": "Sunday",
                "events": [
                    {
                        "name": "Gym Session",
                        "time": "07:00 AM - 08:00 AM"
                    }
                ]
            },
            {
                "day": "Monday",
                "events": [
                    {
                        "name": "Study - APS 100",
                        "time": "08:00 AM - 09:30 AM"
                    },
                    {
                        "name": "Break",
                        "time": "09:30 AM - 10:00 AM"
                    },
                    {
                        "name": "Study - ECE 300",
                        "time": "10:00 AM - 11:30 PM"
                    },
                    {
                        "name": "Break",
                        "time": "11:30 PM - 12:00 PM"
                    },
                    {
                        "name": "Gym Session",
                        "time": "12:00 PM - 01:00 PM"
                    }
                ]
            },
            {
                "day": "Tuesday",
                "events": [
                    {
                        "name": "Study - APS 100",
                        "time": "08:00 AM - 09:30 AM"
                    },
                    {
                        "name": "Break",
                        "time": "09:30 AM - 10:00 AM"
                    },
                    {
                        "name": "Study - ECE 300",
                        "time": "10:00 AM - 11:30 PM"
                    },
                    {
                        "name": "Break",
                        "time": "11:30 PM - 12:00 PM"
                    },
                    {
                        "name": "Gym Session",
                        "time": "12:00 PM - 01:00 PM"
                    }
                ]
            },
            {
                "day": "Wednesday",
                "events": [
                    {
                        "name": "APS 100 Exam",
                        "time": "04:00 PM - 06:00 PM"
                    }
                ]
            },
            {
                "day": "Thursday",
                "events": [
                    {
                        "name": "Study - APS 100",
                        "time": "08:00 AM - 09:30 AM"
                    },
                    {
                        "name": "Break",
                        "time": "09:30 AM - 10:00 AM"
                    },
                    {
                        "name": "Study - ECE 300",
                        "time": "10:00 AM - 11:30 PM"
                    },
                    {
                        "name": "Break",
                        "time": "11:30 PM - 12:00 PM"
                    },
                    {
                        "name": "Gym Session",
                        "time": "12:00 PM - 01:00 PM"
                    }
                ]
            },
            {
                "day": "Friday",
                "events": [
                    {
                        "name": "ECE 300 Exam",
                        "time": "07:00 PM - 09:00 PM"
                    }
                ]
            },
            {
                "day": "Saturday",
                "events": [
                    {
                        "name": "Gym Session",
                        "time": "07:00 AM - 08:00 AM"
                    }
                ]
            }
        ]
    });
    */}

    const daysOfWeek = [ "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    
    const scheduleObject = events.schedule.reduce((acc, entry) => {
        acc[entry.day] = entry.events;
        return acc;
    }, {});

    console.log(scheduleObject["Monday"])

    return (
        <div className="calendar">
            <h2>{currentDate.toLocaleDateString("en-US", { month: "long", year: "numeric" })}</h2>

            <div className="days-grid">
                {daysOfWeek.map((day, index) => (
                    <div key={index} className="day">
                        <h3>{day.toUpperCase()}</h3>
                        {scheduleObject[day] ? (
                            <ul className="events">
                                {scheduleObject[day].map((event, idx) => (
                                    <li key={idx}>{event.name} - {event.time}</li>
                                ))}
                            </ul>
                        ) : (
                            <p>No events</p>
                        )}
                    </div>
                ))}
            </div>

        </div>
    );
}

export default Planner;
