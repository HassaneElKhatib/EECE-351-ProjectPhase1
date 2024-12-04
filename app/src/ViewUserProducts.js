import React, { useState } from "react";
import { Button, TextField, Box, Typography, Stack, Card, CardContent } from "@mui/material";

export default function ViewUserProducts() {
    const [username, setUsername] = useState("");
    const [products, setProducts] = useState([]);
    const [errorMessage, setErrorMessage] = useState("");

    const handleViewUserProducts = async () => {
    
        if (username) {
            try {
                const response = await fetch("http://127.0.0.1:30000/view_user_products", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ username }),
                });
                if (response.ok) {
                    const data = await response.json();
                    setProducts(data.products || []);
                    setErrorMessage("");
                } else {
                    const errorData = await response.json();
                    setErrorMessage(errorData.message || "Failed to fetch products.");
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
                <Typography variant="h4">View User Products</Typography>
                <TextField
                    label="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />
                {errorMessage && <Typography color="error">{errorMessage}</Typography>}
                <Button variant="contained" onClick={handleViewUserProducts}>
                    View Products
                </Button>
                <Box>
                    <Typography variant="h5">Products:</Typography>
                    {products.length > 0 ? (
                        products.map((product, index) => (
                            <Card key={index}>
                                <CardContent>
                                    <Typography variant="h6">{product.name}</Typography>
                                    <Typography>Price: ${product.price}</Typography>
                                    <Typography>{product.description}</Typography>
                                </CardContent>
                            </Card>
                        ))
                    ) : (
                        <Typography>No products found.</Typography>
                    )}
                </Box>
            </Stack>
        </Box>
    );
}
