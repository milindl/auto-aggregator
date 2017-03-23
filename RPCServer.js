var jayson = require("jayson");
const pg = require("pg");
const graph = require("fbgraph");

"use strict";

// Refactor
const access_token = process.env.SHARE_AUTO_FB_ACCESS_TOKEN ||
                     "EAACEdEose0cBABzAsGNcDk1uSYGp5k88OmtwEu9T3zzZBnrqo483uFEpWu1Rb6G66a88myHbRfVVrylr5TBIdjGQp6sf9NJB5o5YSe80VbeDG8wDZBdLyYfFghQKtMjZCGhvtfHua1IiEZC31uLTCUYMGzCcqShGwr6WXjjZCrCZAR33YJ3ZBynyYqCkEp9bRrYZD"
const group_id = process.env.SHARE_AUTO_GROUP_ID || "1304156202997238";
const port = parseInt(process.env.SHARE_AUTO_RPC_SERVER_PORT)||
             6800;

const pool = new pg.Pool();
graph.setAccessToken(access_token);
graph.setVersion("2.3");
const server = jayson.server({
  add: function(args, callback) {
    pool.connect((err, client, done) => {
      if (err) {
	console.log(err);
	done();
	callback(err);
      }
      const results = [];
      const query = client.query("SELECT * " +
				 "FROM posts " +
				 "ORDER BY date ASC;");
      query.on("row", row => results.push(row));
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
