import "./styles/finance.css"
import React, { useState, useRef } from "react";

function AudioRecorder() {
    const [audioUrl, setAudioUrl] = useState(null);
    const mediaRecorderRef = useRef(null);

    const startRecording = async () => {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorderRef.current = new MediaRecorder(stream);
        let audioChunks = []; // 🔹 Reset audio chunks on each start

        mediaRecorderRef.current.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };

        mediaRecorderRef.current.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
            const url = URL.createObjectURL(audioBlob);
            setAudioUrl(url);
        };

        mediaRecorderRef.current.start();
    };

    const stopRecording = () => {
        mediaRecorderRef.current.stop();
    };

    return (
        <div>
            <h2>🎙 Audio Recorder</h2>
            <button onClick={startRecording}>Start Recording</button>
            <button onClick={stopRecording}>Stop Recording</button>
            {audioUrl && <audio controls src={audioUrl}></audio>}
        </div>
    );
}

export default AudioRecorder;
