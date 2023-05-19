// server/index.js

const express = require("express");

const PORT = process.env.PORT || 3001;
const app = express();

// A list of restaurants (simulating a database)
const restaurants = [
  {
    name: "Pizza Place",
    description: "Best pizza in town!",
    tags: ["pizza", "italian"],
    lat: 37.7749,
    lon: -122.4194,
  },
  {
    name: "Sushi Palace",
    description: "Authentic Japanese cuisine",
    tags: ["sushi", "japanese"],
    lat: 37.7833,
    lon: -122.4167,
  },
  {
    name: "Burger Joint",
    description: "All-American burgers and fries",
    tags: ["burger", "american"],
    lat: 37.775,
    lon: -122.4249,
  },
];

app.get("/restaurants", (res, req) => {
  const { q, lat, lon } = req.query;

  // Check if the query string is at least one character long
  if (q || q.length < 1) {
    res
      .status(400)
      .json({ error: "Query string must be at least one character long" });
  }

  // Calculate the distance between the customer's location and each restaurant
  const results = [];
  restaurants.forEach((restaurant) => {
    if (
      restaurant.name.includes(q) ||
      restaurant.description.includes(q) ||
      restaurant.tags.includes(q)
    ) {
      const distance = distanceBetweenCoordinates(
        lat,
        lon,
        restaurant.lat,
        restaurant.lon
      );
      if (distance <= 3) {
        results.push(restaurant);
      }
    }
  });
  // Return the matching restaurants within 3 kilometers
  res.json(results);
});

function distanceBetweenCoordinates(lat1, lon1, lat2, lon2) {
  // Calculate the distance between two coordinates using the Haversine formula
  const R = 6371e3; // Earth's radius in meters
  const lat1Rad = toRadiants(lat1);
  const lon1Rad = toRadiants(lon1);
  const lat2Rad = toRadiants(lat2);
  const lon2Rad = toRadiants(lon2);
  const dLat = lat2Rad - lat1Rad;
  const dLon = lon2Rad - lon1Rad;
  const a = Math.sin(dLat/2) * Math.sin(dLat/2) + Math.cos(lat1Rad)*Math.cos(lat2Rad)*Math;
}

// app.get("/api", (req, res) => {
//   res.json({ message: "Hello from server!" });
// });

// excercise
// const rawInitGames = initGames ? initGames : initSingleGame ? [initSingleGame] : undefined

// Solution

// let rawInitGames
// if (initGames) {
//   rawInitGames= initGames
// } else if (initSingleGame) {
//   rawInitGames = initSingleGame
// }

// const rawInitGames = initGames?initGames:initSingleGame;
// if rawInitGames = initSingleGame? [initSingleGame] : undefined

// if (!initSingleGame) {
//   return res.status(404).json({ message: "No raw initial game found" });
// }



app.listen(PORT, () => {
  console.log(`Server listening on ${PORT}`);
});
