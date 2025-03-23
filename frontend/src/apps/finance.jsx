import "./styles/finance.css"
import React, { useState } from "react";
import axios from "axios";

function Finance() {
    const [responseMessage, setResponseMessage] = useState("");
    const [userMessage, setUserMessage] = useState("");
    const [userImage, setUserImage] = useState();

    const handleSendMessage = async () => {
        try {
            const response = await axios.post("https://plan-974351744512.us-central1.run.app/api/chat", {
                message: userMessage, 
            });

            setResponseMessage(response.data.data);  
            console.log(response.data.data)
        } catch (error) {
            console.error("Error:", error);
            setResponseMessage("Error sending the message.");
        }
    };

    const handleImageChange = (e) => {
        const file = e.target.files[0];  // Get the first selected file
        if (file) {
            console.log("here")
            setUserImage(file);  // Store the file in state
        }
    };

    const convertToBase64 = (file) => {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onloadend = () => resolve(reader.result); // When conversion is done, resolve promise with base64
            reader.onerror = reject;  // If there's an error during conversion, reject promise
            reader.readAsDataURL(file);  // Convert the file to base64
        });
    };

    // Function to send image and text to the Gemini API
    const handleSendImage = async () => {
        if (!userImage) {
            setResponseMessage("Please select an image to upload.");
            return;
        }

        try {
            // Convert the image file to base64
            const base64Image = await convertToBase64(userImage);
            console.log(base64Image)
            const prompt = "Describe what this image contains, text-wise";

            // Prepare the data for Gemini API
            const requestData = {
                parts: [
                    { text: prompt },
                    { inlineData: { data: base64Image.split(",")[1], mimeType: "image/png" } },
                ],
            };

            // Send the request to Gemini API
            const response = await axios.post("https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=AIzaSyAhsIhD2mKoQG1XF_ESl6uhvts15SzGNMY", requestData, {
                headers: {
                    "Content-Type": "application/json",
                },
            });

            // Handle the response from the Gemini API
            const resultText = response.data.response.text;
            setResponseMessage(resultText);  // Display the result
            console.log(resultText);  // Log the result for debugging
        } catch (error) {
            console.error("Error:", error);
            setResponseMessage("Error sending the image.");
        }
    };

    return (
        <div>
            <input type="text" placeholder="Enter your message" value={userMessage} onChange={(e) => setUserMessage(e.target.value)}/>
            <button onClick={handleSendMessage}>Send Message</button>
            <input type="file" placeholder="Upload image" accept="image/*" onChange={handleImageChange}/>
            <button onClick={handleSendImage}>Send Message</button>
            {responseMessage && <p>{responseMessage}</p>}
        </div>
    );
}

export default Finance;
