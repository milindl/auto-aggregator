#!/bin/env node

var jayson = require("jayson");
const pg = require("pg");

"use strict";

// Refactor
const group_id = process.env.SHARE_AUTO_GROUP_ID || "1304156202997238";
const port = parseInt(process.env.SHARE_AUTO_RPC_SERVER_PORT)||
             6800;
const user = process.env.SHARE_AUTO_PGUSER || 'postgres';
const database = process.env.SHARE_AUTO_PGDATABASE || 'postgres';
const password = process.env.SHARE_AUTO_PGPASSWORD || '';
const host = process.env.SHARE_AUTO_PGHOST || 'localhost';
const pgPort = process.env.SHARE_AUTO_PGPORT || 5432;

const config = {
  user: user,
  database: database,
  password: password,
  host: host,
  port: pgPort,
  max: 10, // max number of clients in the pool
  idleTimeoutMillis: 30000, // how long a client is allowed to remain idle before being closed
};

const pool = new pg.Pool(config);
const server = jayson.server({
  get: function(args, callback) {
    pool.connect((err, client, done) => {
      console.log("Logging Request...")
      if (err) {
	console.log(err);
	done();
	callback(err);
      }
      const results = [];
      const query = client.query("SELECT * " +
				 "FROM posts " +
				 "ORDER BY date ASC;");
      query.on("row", row => {results.push(row); console.log(row)});
      query.on("end", () => {
	done();
	// console.log(results);
	callback(null, results);
      });
    });
  }
});

console.log("Starting server...");
server.http().listen(port);
