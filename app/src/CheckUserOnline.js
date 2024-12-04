import React, { useState } from "react";
import { Button, TextField, Box, Typography, Stack } from "@mui/material";

export default function CheckUserOnline({ onSnackbarOpen }) {
    const [username, setUsername] = useState("");
    const [statusMessage, setStatusMessage] = useState("");
    const [errorMessage, setErrorMessage] = useState("");

    const handleCheckOnline = async () => {
        if (username) {
            try {
                const response = await fetch("http://127.0.0.1:30000/check_online", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ username }),
                });
                if (response.ok) {
                    const data = await response.json();
                    setStatusMessage(data.message || "");
                    setErrorMessage("");
                } else {
                    const errorData = await response.json();
                    setErrorMessage(errorData.message || "Failed to check user status.");
                }
            } catch (error) {
                setErrorMessage("An error occurred. Please try again.");
            }
        } else {
            setErrorMessage("Username is required.");
        }
    };

    return (
        <Box sx={{ padding: 4 }}>
            <Stack spacing={2}>
                <Typography variant="h4">Check User Online</Typography>
                <TextField
                    label="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />
                {errorMessage && <Typography color="error">{errorMessage}</Typography>}
                <Button variant="contained" onClick={handleCheckOnline}>
                    Check Online
                </Button>
                {statusMessage && <Typography>{statusMessage}</Typography>}
            </Stack>
        </Box>
    );
}
