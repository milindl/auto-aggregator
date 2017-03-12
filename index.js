const express = require("express");
const bodyParser = require("body-parser");
const api = require("./api/db");

const app = express();
app.use(bodyParser.json());
app.use("/api", api);

console.log("Starting server...");
app.listen(6700);
