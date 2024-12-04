import React, { useState, useEffect } from "react";
import {
    AppBar,
    Toolbar,
    Typography,
    Box,
    Button,
    Dialog,
    Snackbar,
    Alert,
    Card,
    CardMedia,
    CardContent,
    Grid2,
} from "@mui/material";
import Login from "./Login";
import Register from "./Register";
import Logout from "./Logout";
import InsertProduct from "./InsertProduct";
import RemoveProduct from "./RemoveProduct";
import UpdateProduct from "./UpdateProduct";
import BuyProduct from "./BuyProduct";
import ViewBuyers from "./ViewBuyers";

export default function SearchAppBar() {
    const [isRegistered, setIsRegistered] = useState(false);
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [products, setProducts] = useState([]);
    const [selectedProduct, setSelectedProduct] = useState(null);
    const [openDialog, setOpenDialog] = useState(null);
    const [snackbarMessage, setSnackbarMessage] = useState(null);
    const [username, setUsername] = useState(null);

    const openSnackbar = (message, severity = "success") => {
        setSnackbarMessage({ message, severity });
    };

    const closeSnackbar = () => {
        setSnackbarMessage(null);
    };

    const handleDialogClose = () => {
        setOpenDialog(null);
        setSelectedProduct(null);
    };

    const handleRegisterSuccess = () => {
        setIsRegistered(true);
        setOpenDialog(null);
        openSnackbar("Registration successful!", "success");
    };

    const handleLoginSuccess = (newUsername) => {
        setUsername(newUsername);
        setIsLoggedIn(true);
        setOpenDialog(null);
        openSnackbar("Login successful!", "success");
        fetchProducts();
    };

    const handleLogoutSuccess = () => {
        setIsLoggedIn(false);
        setUsername(null);
        setOpenDialog(null);
        setProducts([]);
        openSnackbar("Logout successful!", "success");
    };

    const fetchProducts = async () => {
        if (!isLoggedIn) return
        try {
            const response = await fetch("http://127.0.0.1:30000/view_all_products", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                },
            });
            const data = await response.json();
            console.log("Products fetched:", data); 
            if (response.ok) {
                setProducts(data.products || []);
            } else {
                openSnackbar("Failed to fetch products.", "error");
            }
        } catch (error) {
            console.error("Error fetching products:", error);
            openSnackbar("Error fetching products.", "error");
        }
    };
    

    useEffect(() => {
        if (isLoggedIn) {
            fetchProducts();
            console.log("Fetching products...");
        }
    }, [isLoggedIn]);

    return (
        <Box>
            {/* Snackbar */}
            <Snackbar
                open={Boolean(snackbarMessage)}
                autoHideDuration={6000}
                onClose={closeSnackbar}
            >
                {snackbarMessage && (
                    <Alert onClose={closeSnackbar} severity={snackbarMessage.severity}>
                        {snackbarMessage.message}
                    </Alert>
                )}
            </Snackbar>

            {/* Dialogs */}
            <Dialog open={openDialog === "login"} onClose={handleDialogClose}>
                <Login onSuccessfulLogin={handleLoginSuccess} fetchProducts={fetchProducts} />
            </Dialog>
            <Dialog open={openDialog === "register"} onClose={handleDialogClose}>
                <Register onSuccessfulRegistration={handleRegisterSuccess} />
            </Dialog>
            <Dialog open={openDialog === "logout"} onClose={handleDialogClose}>
                <Logout onSuccessfulLogout={handleLogoutSuccess} />
            </Dialog>
            <Dialog open={openDialog === "insertProduct"} onClose={handleDialogClose}>
                <InsertProduct
                    username={username}
                    onSnackbarOpen={openSnackbar}
                    onClose={handleDialogClose}
                    onProductChange={fetchProducts}
                />
            </Dialog>
            <Dialog open={openDialog === "removeProduct"} onClose={handleDialogClose}>
                <RemoveProduct
                    username={username} 
                    productName={products.name} 
                    onSnackbarOpen={openSnackbar}
                    onProductChange={fetchProducts}
                />
            </Dialog>
            <Dialog open={openDialog === "updateProduct"} onClose={handleDialogClose}>
                <UpdateProduct
                    username={username}
                    onSnackbarOpen={openSnackbar}
                    onClose={handleDialogClose}
                    onProductChange={fetchProducts}
                />
            </Dialog>
            <Dialog open={openDialog === "viewBuyers"} onClose={handleDialogClose}>
                <ViewBuyers
                    username={username}
                    onClose={handleDialogClose}
                    onSnackbarOpen={openSnackbar}
                />
            </Dialog>
            <Dialog open={Boolean(selectedProduct)} onClose={handleDialogClose}>
                {selectedProduct && (
                    <BuyProduct
                        product={selectedProduct}
                        username={username} 
                        onSnackbarOpen={openSnackbar}
                        onClose={handleDialogClose}
                        onProductChange={fetchProducts}
                    />
                )}
            </Dialog>
            {/* AppBar */}
            <AppBar position="fixed" sx={{ bgcolor: "green" }}>
                <Toolbar sx={{ justifyContent: "space-between" }}>
                    <Typography variant="h6" component="div" sx={{ color: "white" }}>
                        AUBoutique
                    </Typography>
                    <Box sx={{ display: "flex", gap: 1 }}>
                        {!isLoggedIn ? (
                            <>
                                <Button
                                    sx={{ color: "white", width: 100 }}
                                    variant="contained"
                                    onClick={() => setOpenDialog("login")}
                                >
                                    Login
                                </Button>
                                <Button
                                    sx={{ color: "white", width: 100 }}
                                    variant="contained"
                                    onClick={() => setOpenDialog("register")}
                                >
                                    Register
                                </Button>
                            </>
                        ) : (
                            <>
                                <Button
                                    sx={{ color: "white", width: 150 }}
                                    variant="contained"
                                    onClick={() => setOpenDialog("insertProduct")}
                                >
                                    Insert Product
                                </Button>
                                <Button
                                    sx={{ color: "white", width: 150 }}
                                    variant="contained"
                                    onClick={() => setOpenDialog("viewBuyers")}
                                >
                                    View Buyers
                                </Button>
                                <Button
                                    sx={{ color: "white", width: 150 }}
                                    variant="contained"
                                    onClick={() => setOpenDialog("logout")}
                                    color="error"
                                >
                                    Logout
                                </Button>
                            </>
                        )}
                    </Box>
                </Toolbar>
            </AppBar>

            {/* Main Content */}
            <Box sx={{ mt: 10, padding: 2 }}>
                {products.length === 0 ? (
                    <Typography variant="h6" color="text.secondary">
                    </Typography>
                ) : (
                    <Grid2 container spacing={20}>
                    {products.map((product) => (
                        <Grid2 item xs={12} sm={6} md={4} key={product.name}>
                            <Card
                                sx={{
                                    display: "flex",
                                    flexDirection: "column",
                                    justifyContent: "space-between",
                                    boxShadow: 3,
                                    "&:hover": { boxShadow: 6 },
                                    maxWidth: 345,
                                    height: 400,
                                    width: "175%",
                                    margin: "auto",
                                }}
                            >
                                <CardMedia
                                    component="img"
                                    image={(function getImage() {
                                        try {
                                            return require(`./images/${product.picture}`);
                                        } catch (err) {
                                            console.error(`Error loading image: ${product.picture}`, err);
                                            return require(`./images/default.png`); 
                                        }
                                    })()}
                                    alt={product.name}
                                    sx={{ height: 145, objectFit: "contain" }}

                                />
                                <CardContent>
                                    <Typography variant="h6">{product.name}</Typography>
                                    <Typography variant="body2">Owner: {product.username}</Typography>
                                    <Typography variant="body2" color="text.secondary">
                                        {product.description}
                                    </Typography>
                                    <Typography variant="body1" color="text.primary">
                                        Price: ${product.price.toFixed(2)}
                                    </Typography>
                                    <Typography variant="body2" color="text.secondary">
                                        Available Quantity: {product.quantity}
                                    </Typography>
                                </CardContent>
                                {username === product.username && ( 
                                    <>
                                        <RemoveProduct
                                            username={username}
                                            productName={product.name}
                                            onSnackbarOpen={openSnackbar}
                                            onProductChange={fetchProducts}
                                        />
                                        <Button
                                            variant="contained"
                                            color="warning"
                                            fullWidth
                                            onClick={() => setOpenDialog("updateProduct")}
                                        >
                                            Update Product
                                        </Button>
                                    </>
                                )}
                                <Button
                                    variant="contained"
                                    color="primary"
                                    fullWidth
                                    onClick={() => setSelectedProduct(product)}
                                >
                                    Buy Now
                                </Button>
                            </Card>
                        </Grid2>
                    ))}
                </Grid2>
                )}
            </Box>
        </Box>
    );
}
