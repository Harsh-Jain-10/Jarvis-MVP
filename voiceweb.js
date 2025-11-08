// jarvis/static/voiceweb.js (Adjusted for new UI)

document.addEventListener('DOMContentLoaded', () => {
    const micButton = document.getElementById('mic-button');
    // const sendButton = document.getElementById('send-button'); // REMOVED
    // const userInput = document.getElementById('user-input'); // REMOVED
    const logContainer = document.getElementById('log'); // This is now the hidden log
    const ringContainer = document.getElementById('ring-container');
    const statusMessage = document.getElementById('status-message');

    // Check for necessary Web Speech API support
    const recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const synth = window.speechSynthesis;
    const speechSupported = recognition && synth;
    
    let isListening = false;
    let currentRecognition = null; // Holds the active recognition object

    // --- State Management ---
    function updateState(newState) {
        ringContainer.classList.remove('idle', 'listening', 'speaking');
        ringContainer.classList.add(newState);

        if (newState === 'listening') {
            statusMessage.textContent = 'Listening...';
            micButton.disabled = true;
            isListening = true;
        } else if (newState === 'speaking') {
            statusMessage.textContent = 'Jarvis is speaking...';
            micButton.disabled = true;
            isListening = false;
        } else {
            statusMessage.textContent = speechSupported 
                ? 'Available...' // Simplified status
                : 'Speech API not supported. Log only.';
            micButton.disabled = false;
            isListening = false;
        }
    }

    // --- Conversation Log Helper (Adjusted for hidden log) ---
    function appendMessage(sender, text, isTranscription = false) {
        // Find the last user message to update transcription, otherwise create new
        if (isTranscription && sender === 'user') {
            const lastUserMsg = logContainer.querySelector('.user-msg:last-child');
            if (lastUserMsg && lastUserMsg.classList.contains('transcribing')) {
                lastUserMsg.textContent = "You: " + text;
                logContainer.scrollTop = logContainer.scrollHeight; // Keep scrolling for transcription
                return;
            }
        }
        
        const p = document.createElement('p');
        p.className = sender === 'user' ? 'user-msg' : 'jarvis-msg';
        p.textContent = (sender === 'jarvis' ? 'Jarvis: ' : 'You: ') + text;
        
        if (isTranscription) {
             p.classList.add('transcribing');
        } else {
             const lastTranscribing = logContainer.querySelector('.user-msg.transcribing');
             if (lastTranscribing) lastTranscribing.classList.remove('transcribing');
        }

        logContainer.appendChild(p);
        logContainer.scrollTop = logContainer.scrollHeight; // Auto-scroll
    }

    // --- Core Communication Function ---
    async function sendQuery(query) {
        if (!query.trim()) return;

        appendMessage('user', query); // Still append to the hidden log
        // userInput.value = ''; // REMOVED
        
        // Stop any currently running recognition
        if (currentRecognition) {
            currentRecognition.stop();
        }

        try {
            updateState('speaking');
            
            const response = await fetch('/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: query })
            });

            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }

            const data = await response.json();
            const replyText = data.reply || "I seem to be having trouble processing that request.";
            
            appendMessage('jarvis', replyText);

            // Use Browser SpeechSynthesis to vocalize server reply
            if (synth) {
                const utterance = new SpeechSynthesisUtterance(replyText);
                utterance.pitch = 1.0;
                utterance.rate = 1.0;
                utterance.onend = () => {
                    updateState('idle'); // Back to idle after browser speech ends
                };
                utterance.onerror = (event) => {
                     console.error('SpeechSynthesis Utterance Error:', event.error);
                     updateState('idle'); // Fallback to idle if speech synthesis fails
                };
                synth.speak(utterance);
            } else {
                 updateState('idle');
            }

        } catch (error) {
            console.error("Communication Error:", error);
            appendMessage('jarvis', `Connection error: ${error.message}. Please check the Flask server.`);
            updateState('idle');
        }
    }

    // --- Voice Recognition Logic ---
    function startListening() {
        if (isListening || !speechSupported) return;

        currentRecognition = new recognition();
        currentRecognition.lang = 'en-US';
        currentRecognition.interimResults = true; // Show results while speaking
        currentRecognition.continuous = false; // Stop after a pause
        
        currentRecognition.onstart = () => {
            updateState('listening');
        };

        currentRecognition.onresult = (event) => {
            const result = event.results[event.results.length - 1];
            const transcript = result[0].transcript;
            
            if (result.isFinal) {
                // Final result received, send to server
                sendQuery(transcript);
            } else {
                // Interim result, update the log with transcription status
                appendMessage('user', transcript, true); 
            }
        };

        currentRecognition.onerror = (event) => {
            console.error('Speech Recognition Error:', event.error);
            updateState('idle');
            if (event.error !== 'no-speech') {
                 appendMessage('jarvis', `Voice recognition error: ${event.error}. Please try typing or check mic permissions.`);
            }
        };

        currentRecognition.onend = () => {
            // If the recognition ended but a final query wasn't sent (e.g., quiet, no speech)
            if (isListening) { 
                updateState('idle'); // Only go idle if we were actively listening
            }
        };

        // Clear previous messages and start recognition
        const lastTranscribing = logContainer.querySelector('.user-msg.transcribing');
        if(lastTranscribing) lastTranscribing.classList.remove('transcribing');
        
        try {
            currentRecognition.start();
        } catch (e) {
            console.error("Recognition start failed:", e);
            updateState('idle');
        }
    }

    // --- Event Listeners ---
    micButton.addEventListener('click', () => {
        if (!isListening) {
            startListening();
        } else {
            // Force stop
            if (currentRecognition) {
                currentRecognition.stop();
            }
            updateState('idle');
        }
    });

    // Removed sendButton and userInput event listeners
    // sendButton.addEventListener('click', () => {
    //     sendQuery(userInput.value);
    // });
    // userInput.addEventListener('keypress', (e) => {
    //     if (e.key === 'Enter') {
    //         sendQuery(userInput.value);
    //     }
    // });

    // Optional: Add a keyboard shortcut to show/hide the debug log (e.g., 'L' key)
    document.addEventListener('keydown', (e) => {
        if (e.key === 'l' || e.key === 'L') {
            logContainer.classList.toggle('visible');
        }
    });


    // Initial state setup
    updateState('idle');
});