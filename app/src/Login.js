import React, { useState } from "react";
import { Button, TextField, Box, Typography, Stack, CircularProgress } from "@mui/material";

export default function Login({ onSuccessfulLogin, fetchProducts, errorMessage = "" }) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [error, setErrorMessage] = useState("");

    async function sendLoginInfo() {
        if (username.trim() && password.trim()) {
            setIsLoading(true);
            setErrorMessage("");

            try {
                const response = await fetch("http://127.0.0.1:30000/login", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ username, password }),
                });

                const data = await response.json();
                if (response.ok && data.message === "Login successful") {
                    console.log("Login successful:", data);
                    console.log(`Client IP: ${data.ip}, Client Port: ${data.port}`);
                    localStorage.setItem("userInfo", JSON.stringify({ username, ip: data.ip, port: data.port }));
                    onSuccessfulLogin(data.username, data.ip, data.port);
                    fetchProducts();
                } else {
                    setErrorMessage(data.message || "Login failed");
                }
            } catch (error) {
                console.error("Error during login:", error);
                setErrorMessage("Login error occurred.");
            } finally {
                setIsLoading(false);
            }
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
            <Stack gap={2} justifyContent={"center"} display={"flex"} alignItems={"center"}>
                <Typography variant="h4" paddingBottom={1}>
                    Login
                </Typography>
                <TextField
                    required
                    sx={{ width: 400 }}
                    label="Username"
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />
                <TextField
                    required
                    sx={{ width: 400 }}
                    label="Password"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                {errorMessage && (
                    <Typography variant="body2" color="error">
                        {errorMessage}
                    </Typography>
                )}
                <Button
                    sx={{ width: "100%" }}
                    variant="contained"
                    onClick={sendLoginInfo}
                    disabled={isLoading}
                >
                    {isLoading ? <CircularProgress size={24} color="inherit" /> : "Login"}
                </Button>
            </Stack>
        </Box>
    );
}
