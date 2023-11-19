const tf = require("@tensorflow/tfjs-node");
const tfjs = require("@tensorflow/tfjs");
module.exports = async function fetchResults(modelPath, fileBuffer) {
  const imageTensor = imageToTensor(fileBuffer);
  const model = await tf.loadLayersModel(modelPath);

  const predictions = await model.predict(tfjs.tensor(imageTensor));
  predictions = predictions.arraySync(); //array contains probability of digits
  predictions = predictions[0]; //it is a rank 2 tensor so converting it to an array
  console.log(predictions);
};
