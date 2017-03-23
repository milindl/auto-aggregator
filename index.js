const express = require("express");
const api = require("./api/db");

const app = express();
app.use("/api", api);

console.log("Starting server...");
app.listen(6700);
