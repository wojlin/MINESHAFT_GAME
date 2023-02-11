let xValues = JSON.parse(document.body.dataset.memory_x);
let yValues = JSON.parse(document.body.dataset.memory_y);
console.log(xValues);
console.log(yValues);
new Chart("myChart", {
  type: "line",
  data: {
    labels: xValues,
    datasets: [{
      backgroundColor: "rgba(0,0,0,1.0)",
      borderColor: "rgba(0,0,0,0.1)",
      data: yValues
    }]
  },
  options:{}
});