"use strict";

const express = require("express");
const pg = require("pg");
const router = express.Router();
const pool = new pg.Pool();

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
  // TODO: Post to facebook and get author and post_id
  let author = "dummy author";
  let post_id = Math.round(Math.random() * 5000000);
  pool.connect((err, client, done) => {
    if (err) {
      console.log(err);
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
		   author, "", req.body.date, req.body.frm,
		   req.body.to, new Date(), req.body.time, post_id
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
});
module.exports = router;
