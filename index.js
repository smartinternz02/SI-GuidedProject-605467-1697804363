const express = require("express");
const app = express();
const path = require("path");
const ejsMate = require("ejs-mate");
const methodOverride = require("method-override");
const multer = require("multer");

const storage = multer.memoryStorage();
const upload = multer({ storage: storage });

const modelPath = "file://models/alzheimer_detection/model.json";

app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(methodOverride("_method"));
app.use(express.static(path.join(__dirname, "public")));

app.engine("ejs", ejsMate);

app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));

app.listen(8080, () => {
  console.log("listening on 8080");
});

app.get("/", (req, res) => {
  res.render("index");
});

// app.post("/get-result", upload.single("image"), async (req, res) => {
//   const imageBuffer = req.file.buffer;
//   const predictions = await predict(modelPath, imageBuffer);
//   console.log(predictions);
// });
