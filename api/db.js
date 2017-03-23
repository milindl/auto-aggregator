"use strict";

const access_token = "EAACEdEose0cBABzAsGNcDk1uSYGp5k88OmtwEu9T3zzZBnrqo483uFEpWu1Rb6G66a88myHbRfVVrylr5TBIdjGQp6sf9NJB5o5YSe80VbeDG8wDZBdLyYfFghQKMjZCGhvtfHua1IiEZC31uLTCUYMGzCcqShGwr6WXjjZCrCZAR33YJ3ZBynyYqCkEp9bRrYZD"
const group_id = "1304156202997238";

const express = require("express");
const pg = require("pg");
const graph = require("fbgraph");

const router = express.Router();
const pool = new pg.Pool();
graph.setAccessToken(access_token);
graph.setVersion("2.3");
router.get("/posts", (req, res) => {
  pool.connect((err, client, done) => {
    if (err) {
      console.log(err);
      done();
      return res.sendStatus(500);
    }
    const results = [];
    const query = client.query("SELECT * " +
                               "FROM posts " +
                               "ORDER BY date ASC;");
    query.on("row", row => results.push(row));
    query.on("end", () => {
      done();
      // console.log(results);
      return res.status(200).json(results);
    });
  });
});

module.exports = router;
