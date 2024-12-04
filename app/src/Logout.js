import React, { useState } from "react";
import { Button, Box, Typography, Stack, CircularProgress } from "@mui/material";

export default function Logout({ onSuccessfulLogout }) {
    const [isLoading, setIsLoading] = useState(false);
    const [errorMessage, setErrorMessage] = useState("");
    const url = "http://127.0.0.1:30000";

    const handleLogout = async () => {
        const userInfo = JSON.parse(localStorage.getItem("userInfo"));
        if (!userInfo) {
            setErrorMessage("No user information found.");
            return;
        }

        const { username, ip, port } = userInfo;

        setIsLoading(true);
        setErrorMessage("");

        try {
            const response = await fetch(`${url}/logout`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ username, ip, port }),
            });

            if (response.ok) {
                const data = await response.json();
                console.log(data);
                localStorage.removeItem("userInfo");
                onSuccessfulLogout();
            } else {
                const errorData = await response.json();
                setErrorMessage(errorData.message || "Logout failed.");
            }
        } catch (error) {
            console.error("Error during logout:", error);
            setErrorMessage("An error occurred during logout. Please try again.");
        } finally {
            setIsLoading(false);
        }
    };

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
                    Logout
                </Typography>
                {errorMessage && (
                    <Typography variant="body2" color="error">
                        {errorMessage}
                    </Typography>
                )}
                <Button
                    sx={{ width: "100%" }}
                    variant="contained"
                    color="error"
                    onClick={handleLogout}
                    disabled={isLoading}
                >
                    {isLoading ? <CircularProgress size={24} color="inherit" /> : "Logout"}
                </Button>
            </Stack>
        </Box>
    );
}
