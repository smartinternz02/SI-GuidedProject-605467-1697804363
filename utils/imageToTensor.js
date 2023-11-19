const tf = require("@tensorflow/tfjs-node");
const fs = require("fs").promises;

module.exports = function imageToTensor(imageBuffer, width, height) {
  const tensor = tf.node.decodeImage(imageBuffer);
  return tensor;
};
