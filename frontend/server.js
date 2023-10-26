const express = require("express");
const path = require("path");
const app = express();

app.use(express.static(__dirname + "/public/"));

app.get("/", async(req, res) => {
    res.sendFile(path.join(__dirname, "public", "index.html"));
});

app.listen(3000, () => {
    console.log("Server running on port 3000");
});