"use strict";

const group_id = "1304156202997238";

const express = require("express");
const pg = require("pg");
const graph = require("fbgraph");

const router = express.Router();
const pool = new pg.Pool();
graph.setAccessToken(access_token);
graph.setVersion("2.3");

router.get("/posts", (req, res) => {
  const today = new Date();
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
    console.log(today);
    query.on("row", row => results.push(row));
    query.on("end", () => {
      done();
      return res.status(200).json(results);
    });
  });
});

router.post("/posts", (req, res) => {
  // TODO: REFACTOR URGENTLY, use PROMISES
  const message = [ "To: ", req.body.to, "\n",
                    "From: ", req.body.frm, "\n",
                    "Date: ", new Date(req.body.date).toUTCString()
                                                     .split(" ")
                                                     .slice(0, 4)
                                                     .join(" "),
                    "\n",
                    "Time: ", req.body.time, "\n",
                    "Additional Info: ", req.body.content, "\n"
                  ].join("");
  let postIdPromise = new Promise((resolve, reject) => {
    graph.post(`${group_id}/feed`, { message: message },
               (err, result) => {
                 if(err)
                   reject(err);
                 else
                   resolve(result["id"].split("_")[1]);
               });
  });
  let authorPromise = new Promise((resolve, reject) => {
    graph.get("/me?fields=name",
              (err, result) => {
                if (err)
                  reject(err);
                else
                  resolve(result["name"]);
              });
  });
  Promise.all([postIdPromise, authorPromise])
    .then((values) => {
      pool.connect((err, client, done) => {
        // 'to' is a reserved word and needs to be qouted
        const query = client.query("INSERT INTO posts(" +
                                   [
                                     "author", "content", "date", "frm",
                                     "\"to\"", "posting_date", "time", "post_id"
                                   ].join(",") +
                                   ") values($1, $2, $3, $4, $5, $6, $7, $8)",
                                   [
                                     values[1], req.body.content, req.body.date, req.body.frm,
                                     req.body.to, new Date(), req.body.time, values[0]
                                   ]);
        query.on("error", (err) => {
          done();
          console.log(err);
          res.sendStatus(500);
        });
        query.on("end", () => {
          done();
          res.sendStatus(200);
        });
      });
    })
    .catch((err) => {
      console.log(err);
      res.sendStatus(500);
    });
});
module.exports = router;
