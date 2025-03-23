import "./styles/finance.css";
import React, { useState } from "react";
import axios from "axios";

function Finance() {
    const [messageHistory, setMessageHistory] = useState([]); // Stores the history of messages
    const [userMessage, setUserMessage] = useState(""); // Stores the user's current message
    const [userImage, setUserImage] = useState(); // Stores the user's selected image

    const handleSendMessage = async () => {
        if (!userMessage) return; // Don't send if message is empty

        // Add the user message to the message history
        setMessageHistory((prevHistory) => [
            ...prevHistory,
            { type: "sent", message: userMessage }
        ]);

        try {
            const response = await axios.post("https://plan-974351744512.us-central1.run.app/api/chat", {
                message: userMessage, 
            });

            // Add the bot response to the message history
            setMessageHistory((prevHistory) => [
                ...prevHistory,
                { type: "received", message: response.data.data }
            ]);

            setUserMessage(""); // Clear the input field
            console.log(response.data.data);
        } catch (error) {
            console.error("Error:", error);
            setMessageHistory((prevHistory) => [
                ...prevHistory,
                { type: "received", message: "Error sending the message." }
            ]);
        }
    };

    const handleImageChange = (e) => {
        setUserImage(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault(); // Prevent any default behavior (e.g., form submission)

        if (!userImage) {
            setMessageHistory((prevHistory) => [
                ...prevHistory,
                { type: "received", message: "Please select an image." }
            ]);
            return;
        }

        const formData = new FormData();
        formData.append('image', userImage);

        try {
            // Sending the image to the backend
            const response = await fetch('https://planimage-974351744512.us-central1.run.app/api/image', {
                method: 'POST',
                body: formData // Send the image as part of FormData
            });

            if (response.ok) {
                const data = await response.json();
                setMessageHistory((prevHistory) => [
                    ...prevHistory,
                    { type: "sent", message: "Image sent successfully." },
                    { type: "received", message: data.data }
                ]);
            } else {
                const error = await response.json();
                setMessageHistory((prevHistory) => [
                    ...prevHistory,
                    { type: "received", message: "Error: " + error.error }
                ]);
            }
        } catch (error) {
            setMessageHistory((prevHistory) => [
                ...prevHistory,
                { type: "received", message: "Error: " + error.message }
            ]);
        }
    };

    return (
        <div id="finance">
            <div className="chat_history">
                {messageHistory.map((entry, index) => (
                    <div key={index} className={entry.type === "sent" ? "sent chat inter" : "received chat inter"}>
                        {entry.message}
                    </div>
                ))}
            </div>
            
            <div className="form">
            <input id = "text" 
                type="text" 
                placeholder="Enter your message" 
                value={userMessage} 
                onChange={(e) => setUserMessage(e.target.value)} 
            />
            <button onClick={handleSendMessage}/>
            </div>
            <div className="form">
            <input id="image"
                type="file" 
                placeholder="Upload image" 
                accept="image/*" 
                onChange={handleImageChange} 
            />
            <button type="submit" onClick={handleSubmit}/>
            </div>
        </div>
    );
}

export default Finance;
