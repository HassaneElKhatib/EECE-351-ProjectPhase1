import React, { useState } from "react";
import { Button, TextField, Typography, Stack, Box } from "@mui/material";

export default function Register({ onSuccessfulRegistration }) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [email, setEmail] = useState("");
    const [name, setName] = useState("");
    const [address, setAddress] = useState("");
    const [errorMessage, setErrorMessage] = useState("");
    const url = "http://127.0.0.1:30000";

    async function sendRegistrationInfo() {
        if (username && password && email && name && address) {
            try {
                const response = await fetch(`${url}/register`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        username,
                        password,
                        email,
                        name,
                        address,
                    }),
                });

                if (response.ok) {
                    const data = await response.json();
                    console.log("Registration successful:", data);
                    setErrorMessage("");
                    onSuccessfulRegistration(); 
                } else {
                    setErrorMessage("Registration failed");
                }
            } catch (error) {
                console.error("Error during registration:", error);
                setErrorMessage("An error occurred. Please try again.");
            }
        } else {
            setErrorMessage("All fields are required");
        }
    }

    return (
        <Box
            sx={{
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                padding: 4,
            }}
        >
            <Stack spacing={2} alignItems="center" width={500}>
                <Typography variant="h4">Register</Typography>
                <TextField
                    required
                    fullWidth
                    label="Name"
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                />
                <TextField
                    required
                    fullWidth
                    label="Address"
                    type="text"
                    value={address}
                    onChange={(e) => setAddress(e.target.value)}
                />
                <TextField
                    required
                    fullWidth
                    label="Email"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
                <TextField
                    required
                    fullWidth
                    label="Username"
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />
                <TextField
                    required
                    fullWidth
                    label="Password"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                {errorMessage && (
                    <Typography color="error" variant="body2">
                        {errorMessage}
                    </Typography>
                )}
                <Button
                    variant="contained"
                    onClick={sendRegistrationInfo}
                    sx={{ width: "100%", height: "2.5rem" }}
                >
                    Register
                </Button>
            </Stack>
        </Box>
    );
}
