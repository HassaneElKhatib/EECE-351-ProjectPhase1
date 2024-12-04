import {
    Box,
    Stack,
    Typography,
    TextField,
    Button
} from "@mui/material";
import React, {useState} from "react";
export default function BuyProduct({ product, onSnackbarOpen, onClose, onProductChange, username }) {
    const [quantityToBuy, setQuantityToBuy] = useState(0);


    const handleBuyProduct = async () => {
        if (!product || !quantityToBuy || quantityToBuy < 1) {
            onSnackbarOpen("Invalid product or quantity.", "error");
            return;
        }

        try {
            const response = await fetch("http://127.0.0.1:30000/buy_product", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    product_name: product.name,
                    buyer_username: username, 
                    quantity_to_buy: quantityToBuy,
                }),
            });
            const data = await response.json();

            if (response.ok) {
                onSnackbarOpen("Product purchased successfully!", "success");
                onProductChange();
                onClose();
            } else {
                onSnackbarOpen(data.message || "Failed to purchase product.", "error");
            }
        } catch (error) {
            console.error("Error purchasing product:", error);
            onSnackbarOpen("An error occurred during purchase.", "error");
        }
    };

    return (
        <Box sx={{ padding: 4 }}>   
            <Stack spacing={2}>
                <Typography variant="h4">Buy {product?.name}</Typography>
                <Typography variant="body1" color="text.secondary">
                    Description: {product?.description}
                </Typography>
                <Typography variant="body1" color="text.primary">
                    Price: ${product?.price.toFixed(2)}
                </Typography>
                <Typography variant="body1" color="text.secondary">
                    Available Quantity: {product?.quantity}
                </Typography>
                <TextField
                    label="Quantity to Buy"
                    type="number"
                    value={quantityToBuy}
                    onChange={(e) => setQuantityToBuy(Math.max(1, parseInt(e.target.value, 10)))}
                />
                <Button variant="contained" onClick={handleBuyProduct}>
                    Buy Now
                </Button>
                <Button variant="outlined" color="error" onClick={onClose}>
                    Cancel
                </Button>
            </Stack>
        </Box>
    );
}
