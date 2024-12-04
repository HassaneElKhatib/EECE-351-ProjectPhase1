import React from "react";
import { Button } from "@mui/material";

export default function RemoveProduct({ username, productName, onSnackbarOpen, onProductChange }) {
    const handleRemoveProduct = async () => {
        try {
            const response = await fetch("http://127.0.0.1:30000/remove_product", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    username,
                    name: productName, 
                }),
            });

            if (response.ok) {
                onSnackbarOpen("Product removed successfully!", "success");
                onProductChange(); 
            } else {
                const errorData = await response.json();
                onSnackbarOpen(errorData.message || "Failed to remove product.", "error");
            }
        } catch (error) {
            console.error("Error removing product:", error);
            onSnackbarOpen("An error occurred while removing the product.", "error");
        }
    };

    return (
        <Button
            variant="contained"
            color="secondary"
            fullWidth
            onClick={handleRemoveProduct}
        >
            Remove Product
        </Button>
    );
}
