// import dependencies
require("dotenv").config({ path: "../.env" });
const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");
const morgan = require("morgan");
const app = express(); // create your express app
const mongo = require("mongodb");
const MongoClient = mongo.MongoClient;
const uri = process.env.MONGO_NORM_USER;
var client;
var mongoClient = new MongoClient(uri, {
  reconnectTries: Number.MAX_VALUE,
  autoReconnect: true,
  useNewUrlParser: true
});
mongoClient.connect((err, db) => {
  // returns db connection
  if (err != null) {
    console.log(err);
    return;
  }
  client = db;
});

// make app use dependencies
app.use(morgan("dev"));
app.use(bodyParser.json());
app.use(cors());

app.get("/", (req, res) => {
  console.log("The Key Works!");
  console.log(process.env.SERVER_PORT);
  res.send(process.env.SERVER_PORT);
});

//*****NEWS*****//
app.get("/news", (req, res) => {
  const collection = client.db("test").collection("dummy");
  collection.find().toArray(function(err, results) {
    if (err) {
      console.log(err);
      res.send([]);
      return;
    }

    res.send(results);
  });
});

//*****STOCKS*****//
app.get("/stocks", (req, res) => {
  const collection = client.db("test").collection("companies");
  collection
    .find({}, { projection: { ticker: 1, _id: 0 } })
    .toArray(function(err, results) {
      if (err) {
        console.log(err);
        res.send([]);
        return;
      }
      res.send(results);
    });
});

app.get("/stock", (req, res) => {
  const collection = client.db("test").collection(req.query.ticker);
  collection
    .find(
      {},
      {
        projection: {
          ticker: 1,
          close: 1,
          high: 1,
          low: 1,
          open: 1,
          change: 1,
          _id: 1
        }
      }
    )
    .sort({ date: -1 })
    .limit(1)
    .toArray(function(err, results) {
      if (err) {
        console.log(err);
        res.send([]);
        return;
      }
      res.send(results);
    });
});

//*****USERS*****//
app.get("/userStocks", (req, res) => {
  const collection = client.db("test").collection("stocks");
  collection.find().toArray(function(err, results) {
    if (err) {
      console.log(err);
      res.send([]);
      return;
    }

    res.send(results);
  });
});

app.post("/addStock", (req, res) => {
  const collection = client.db("test").collection("users");
  var user = req.body.user; // parse the data from the request's body
  var stock = req.body.stock;
  console.log(req);
  collection.update(
    { email: user },
    { $push: { stocks: { ticker: stock } } },
    { upsert: true }
  );
  res.send();
});

app.post("/deleteUserStock", (req, res) => {
  const collection = client.db("test").collection("stocks");
  // remove document by its unique _id
  collection.removeOne({ _id: mongo.ObjectID(req.body.todoID) }, function(
    err,
    results
  ) {
    if (err) {
      console.log(err);
      res.send("");
      return;
    }
    res.send(); // return
  });
});

//*****TODOS*****//
app.get("/todo", (req, res) => {
  const collection = client.db("test").collection("stocks");
  collection.find().toArray(function(err, results) {
    if (err) {
      console.log(err);
      res.send([]);
      return;
    }

    res.send(results);
  });
});

app.post("/addTodo", (req, res) => {
  const collection = client.db("test").collection("stocks");
  var todo = req.body.todo; // parse the data from the request's body
  collection.insertOne({ title: todo }, function(err, results) {
    if (err) {
      console.log(err);
      res.send("");
      return;
    }
    res.send(results.ops[0]); // returns the new document
  });
});

app.post("/deleteTodo", (req, res) => {
  const collection = client.db("test").collection("stocks");
  // remove document by its unique _id
  collection.removeOne({ _id: mongo.ObjectID(req.body.todoID) }, function(
    err,
    results
  ) {
    if (err) {
      console.log(err);
      res.send("");
      return;
    }
    res.send(); // return
  });
});

/***** LISTEN TO PORT AND HANDLE CTRL+C *****/
app.listen(process.env.PORT || 8081); // client is already running on 8080

process.once("SIGUSR2", function() {
  server.close(function() {
    process.kill(process.pid, "SIGUSR2");
  });
});
