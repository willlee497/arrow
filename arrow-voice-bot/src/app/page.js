'use client';

import { useState, useRef } from 'react';

export default function Home() {
  const [transcript, setTranscript] = useState('');
  const [response, setResponse] = useState('');
  const recognitionRef = useRef(null);

  const startListening = () => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onresult = async (event) => {
      const userInput = event.results[0][0].transcript;
      setTranscript(userInput);

      try {
        const res = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ prompt: userInput }),
        });

        const data = await res.json();
        if (data.response) {
          setResponse(data.response);
          speak(data.response);
        } else {
          setResponse("Sorry, I couldn't respond.");
        }
      } catch (err) {
        console.error('Fetch error:', err);
        setResponse("Error talking to WilliamAI.");
      }
    };

    recognition.onerror = (event) => {
      console.error('Speech recognition error', event);
    };

    recognition.start();
    recognitionRef.current = recognition;
  };

  const speak = (text) => {
    const synth = window.speechSynthesis;
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1;
    utterance.pitch = 1.1;
    utterance.lang = 'en-US';
    synth.speak(utterance);
  };

  return (
    <div className="min-h-screen bg-sky-100 text-black flex flex-col items-center justify-center p-6">
      <h1 className="text-3xl font-bold mb-4">🎙️ Talk to WilliamAI</h1>
      <button
        onClick={startListening}
        className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-full text-lg"
      >
        Start Talking
      </button>
      <div className="mt-6 w-full max-w-2xl">
        <p><strong>You asked:</strong> {transcript}</p>
        <p className="mt-4"><strong>WilliamAI says:</strong> {response}</p>
      </div>
    </div>
  );
}