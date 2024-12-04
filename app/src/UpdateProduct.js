import React, { useState } from "react";
import { Button, TextField, Box, Typography, Stack } from "@mui/material";

export default function UpdateProduct({ username, onSnackbarOpen , onProductChange}) {
    const [name, setName] = useState("");
    const [picture, setPicture] = useState("");
    const [price, setPrice] = useState("");
    const [description, setDescription] = useState("");
    const [quantity, setQuantity] = useState("");
    const [errorMessage, setErrorMessage] = useState("");

    const handleUpdateProduct = async () => {
        if (name && picture && price && description && quantity) {
            try {
                const response = await fetch("http://127.0.0.1:30000/update_product", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        username, 
                        name,
                        picture,
                        price: parseFloat(price),
                        description,
                        quantity,
                    }),
                });
                if (response.ok) {
                    onSnackbarOpen("Product updated successfully!", "success");
                    onProductChange();
                    setErrorMessage("");
                } else {
                    const errorData = await response.json();
                    setErrorMessage(errorData.message || "Failed to update product.");
                }
            } catch (error) {
                setErrorMessage("An error occurred. Please try again.");
            }
        } else {
            setErrorMessage("All fields are required.");
        }
    };
    

    return (
        <Box sx={{ padding: 4 }}>
            <Stack spacing={2}>
                <Typography variant="h4">Update Product</Typography>
                <TextField
                    label="Product Name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                />
                <TextField
                    label="Picture URL"
                    value={picture}
                    onChange={(e) => setPicture(e.target.value)}
                />
                <TextField
                    label="Price"
                    type="number"
                    value={price}
                    onChange={(e) => setPrice(e.target.value)}
                />
                <TextField
                    label="Description"
                    multiline
                    rows={4}
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                />
                <TextField
                    label = "Quantity"
                    type = "number"
                    value={quantity}
                    onChange={(e) => setQuantity(e.target.value)}
                />
                {errorMessage && <Typography color="error">{errorMessage}</Typography>}
                <Button variant="contained" onClick={handleUpdateProduct}>
                    Update Product
                </Button>
            </Stack>
        </Box>
    );
}
