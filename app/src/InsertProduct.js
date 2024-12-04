import React, { useState } from "react";
import { Button, Dialog, TextField, Stack, Typography } from "@mui/material";

export default function InsertProduct({ username, onSnackbarOpen, onClose, onProductChange }) {
    const [productData, setProductData] = useState({
        name: "",
        picture: "",
        price: "",
        description: "",
        quantity: "",
    });
    const [errorMessage, setErrorMessage] = useState("");

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setProductData((prev) => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async () => {
        if (!productData.name || !productData.picture || !productData.price || !productData.description || !productData.quantity) {
            onSnackbarOpen("All fields are required.", "error");
            return;
        }
        try {
            const response = await fetch("http://127.0.0.1:30000/add_product", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ ...productData, username }),
            });
            const data = await response.json();
            if (response.ok) {
                onSnackbarOpen("Product added successfully!", "success");
                onProductChange();
                onClose();
                setProductData({ name: "", picture: "", price: "", description: "" , quantity: ""});
            } else {
                setErrorMessage(data.message || "Failed to add product.");
            }
        } catch (error) {
            setErrorMessage("An error occurred. Please try again.");
        }
    };

    return (
        <Dialog open>
            <Stack spacing={2} sx={{ padding: 3, minWidth: 300 }}>
                <Typography variant="h6">Insert New Product</Typography>
                <TextField
                    label="Product Name"
                    name="name"
                    value={productData.name}
                    onChange={handleInputChange}
                />
                <TextField
                    label="Picture URL"
                    name="picture"
                    value={productData.picture}
                    onChange={handleInputChange}
                />
                <TextField
                    label="Price"
                    name="price"
                    type="number"
                    value={productData.price}
                    onChange={handleInputChange}
                />
                <TextField
                    label="Description"
                    name="description"
                    multiline
                    rows={3}
                    value={productData.description}
                    onChange={handleInputChange}
                />
                <TextField
                    label = "Quantity"
                    name="quantity"
                    type="number"
                    value={productData.quantity}
                    onChange={handleInputChange}
                />
                {errorMessage && (
                    <Typography color="error" variant="body2">
                        {errorMessage}
                    </Typography>
                )}
                <Button variant="contained" color="primary" onClick={handleSubmit}>
                    Submit
                </Button>
            </Stack>
        </Dialog>
    );
}
