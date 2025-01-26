import React, { useState } from "react";

export default function WasteClassifierApp() {
    const [prompt, setPrompt] = useState("");
    const [classification, setClassification] = useState("");
    const [error, setError] = useState("");

    const classifyWaste = async () => {
        try {
            setError("");
            setClassification("");

            if (!prompt) {
                setError("Please enter a description of the waste item.");
                return;
            }

            const response = await fetch("/classify_waste", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ prompt }),
            });

            const data = await response.json();

            if (response.ok) {
                setClassification(data.classification);
            } else {
                setError(data.error || "An error occurred while classifying the waste.");
            }
        } catch (err) {
            setError("Failed to connect to the backend. Ensure it is running.");
        }
    };

    return (
        <div style={{ padding: "20px", maxWidth: "600px", margin: "0 auto" }}>
            <h1>Waste Classification Chatbot</h1>
            <p>Enter a description of your waste item to classify it.</p>

            <div style={{ marginBottom: "10px" }}>
                <textarea
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    placeholder="e.g., banana peel"
                    style={{
                        width: "100%",
                        height: "100px",
                        padding: "10px",
                        borderRadius: "5px",
                        border: "1px solid #ccc",
                    }}
                />
            </div>

            <button
                onClick={classifyWaste}
                style={{
                    padding: "10px 20px",
                    backgroundColor: "#4CAF50",
                    color: "white",
                    border: "none",
                    borderRadius: "5px",
                    cursor: "pointer",
                }}
            >
                Classify Waste
            </button>

            {classification && (
                <div style={{ marginTop: "20px", color: "green", fontWeight: "bold" }}>
                    {classification}
                </div>
            )}

            {error && (
                <div style={{ marginTop: "20px", color: "red", fontWeight: "bold" }}>
                    {error}
                </div>
            )}
        </div>
    );
}
