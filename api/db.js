"use strict";


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

router.post("/posts", async((req, res) => {
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
  graph.post(`${group_id}/feed`, { message: message },
             (err, result) => {
               if (err) {
                 console.log(err);
                 return null;
               }
               let post_id =  result["id"].split("_")[1];
               graph.get("/me?fields=name",
                         (err2, result2) => {
                           if (err2) {
                             console.log(err2);
                             return null;
                           }
                           let author = result2["name"];
                           pool.connect((err3, client, done) => {
                             if (err3) {
                               console.log(err3);
                               done();
                               return res.sendStatus(500);
                             }
                             console.log(req.body);
                             // 'to' is a reserved word and needs to be qouted
                             const query = client.query("INSERT INTO posts(" +
                                                        [
                                                          "author", "content", "date", "frm",
                                                          "\"to\"", "posting_date", "time", "post_id"
                                                        ].join(",") +
                                                        ") values($1, $2, $3, $4, $5, $6, $7, $8)",
                                                        [
                                                          author, req.body.content, req.body.date, req.body.frm,
                                                          req.body.to, new Date(), req.body.time, post_id
                                                        ]);
                             query.on("error", (err4) => {
                               done();
                               console.log(err4);
                               res.sendStatus(500);
                             });
                             query.on("end", () => {
                               done();
                               res.sendStatus(200);
                             });
                           });
                         });
             });
}));
module.exports = router;
