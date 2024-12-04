import React, { useState, useEffect } from "react";
import { Box, Typography, Card, CardMedia, CardContent, Button } from "@mui/material";

export default function Products() {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch("http://127.0.0.1:30000/view_all_products")
            .then((response) => response.json())
            .then((data) => setProducts(data.products || []))
            .catch((error) => console.error("Error fetching products:", error));
    }, []);
    

    if (loading) {
        return <Typography>Loading...</Typography>;
    }

    if (products.length === 0) {
        return <Typography>No products available. Please check back later!</Typography>;
    }

    return (
        <Box display="flex" flexWrap="wrap" justifyContent="center" gap={2} p={2}>
            {products.map((product, index) => (
                <Card key={index} sx={{ width: 300, boxShadow: 3 }}>
                    <CardMedia
                        component="img"
                        height="200"
                        image={product.picture}
                        alt={product.name}
                    />
                    <CardContent>
                        <Typography variant="h6">{product.name}</Typography>
                        <Typography variant="body2" color="text.secondary">
                            {product.description}
                        </Typography>
                        <Typography variant="body1" color="text.primary">
                            Price: ${product.price.toFixed(2)}
                        </Typography>
                        <Button variant="contained" color="primary" fullWidth sx={{ mt: 2 }}>
                            Buy Now
                        </Button>
                    </CardContent>
                </Card>
            ))}
        </Box>
    );
}
