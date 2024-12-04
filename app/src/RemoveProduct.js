import React, { useState } from "react";
import { Button, TextField, Box, Typography, Stack } from "@mui/material";

export default function RemoveProduct({ username, onSnackbarOpen , onProductChange}) {
    const [name, setName] = useState(""); 
    const [errorMessage, setErrorMessage] = useState("");

    const handleRemoveProduct = async () => {
        if (name) {
            try {
                const response = await fetch("http://127.0.0.1:30000/remove_product", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ username, name }), 
                });
                if (response.ok) {
                    onSnackbarOpen("Product removed successfully!", "success");
                    onProductChange();
                    setErrorMessage("");
                } else {
                    const errorData = await response.json();
                    setErrorMessage(errorData.message || "Failed to remove product.");
                }
            } catch (error) {
                setErrorMessage("An error occurred. Please try again.");
            }
        } else {
            setErrorMessage("Product name is required.");
        }
    };
    

    return (
        <Box sx={{ padding: 4 }}>
            <Stack spacing={2}>
                <Typography variant="h4">Remove Product</Typography>
                <TextField
                    label="Product Name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                />
                {errorMessage && <Typography color="error">{errorMessage}</Typography>}
                <Button variant="contained" onClick={handleRemoveProduct}>
                    Remove Product
                </Button>
            </Stack>
        </Box>
    );
}
