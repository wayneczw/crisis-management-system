const brandPrimary = '#6a1a09'
const brandSuccess = '#4dbd74'
const brandInfo = '#63c2de'
const brandDanger = '#f86c6b'
const brandBlack = "#000000"

function convertHex (hex, opacity) {
  hex = hex.replace('#', '')
  const r = parseInt(hex.substring(0, 2), 16)
  const g = parseInt(hex.substring(2, 4), 16)
  const b = parseInt(hex.substring(4, 6), 16)

  const result = 'rgba(' + r + ',' + g + ',' + b + ',' + opacity / 100 + ')'
  return result
}

function random (min, max) {
  return Math.floor(Math.random() * (max - min + 1) + min)
}

    var elements = 10
    console.log(document.getElementById('psi-trend').value.replace(/'/g, "\""))
    var psi_values = JSON.parse(document.getElementById('psi-trend').value.replace(/'/g, "\""));
    // psi example: {'east': ['12', 'Healthy'], 'west': ['10', 'Healthy'], 'sourth': ['13', 'Healthy'],
    // 'north': ['10', 'Healthy'], 'central': ['11', 'Healthy']}

    var dengue_values = JSON.parse(document.getElementById('dengue-trend').value.replace(/'/g, "\""));
    // dengue example: {'Bishan Street 11(Bishan Loft)': ['3', '3'], 'Bukit Batok Street 21(Blk 201)': ['3', '3'],
    // 'Eng Kong Crescent': ['3', '5'], 'Jalan Gelenggang': ['2', '5'], 'Jalan Tenaga(Blk 656)': ['5', '6'],
    // 'Woodlands Avenue 5(Bellewoods)': ['3', '5'], 'Woodlands Circle': ['1', '10'], 'Woodlands Cresent(Blk 787C)': ['5', '5']}

    var data1 = psi_values["east"];
    var data2 = psi_values["west"];
    var data3 = psi_values["north"];
    var data4 = psi_values["sourth"];
    var data5 = psi_values["central"];

    var data6 = dengue_values["2 weeks total"];
    var data7 = dengue_values["overall total"];

    function done(){
      var url= myChart.toBase64Image();
      document.getElementById("trafficChart").href=url;
    }

    //PSI Chart
    function drawPSIChart(){
        console.log('Drawing PSI Chart...');

        var ctx = document.getElementById( "trafficChart" ).getContext("2d");
        ctx.height = 100;
        ctx.width = 150;
        myChart = new Chart( ctx, {
            type: 'line',
            data: {
                labels: generate_times(),
                datasets: [
                {
                  label: 'East',
                  backgroundColor: 'transparent',
                  borderColor: brandInfo,
                  pointHoverBackgroundColor: '#fff',
                  borderWidth: 2,
                  data: data1
              },
              {
                  label: 'West',
                  backgroundColor: 'transparent',
                  borderColor: brandSuccess,
                  pointHoverBackgroundColor: '#fff',
                  borderWidth: 2,
                  data: data2
              },
              {
                  label: 'North',
                  backgroundColor: 'transparent',
                  borderColor: brandDanger,
                  pointHoverBackgroundColor: '#fff',
                  borderWidth: 2,
                  data: data3
              },
              {
                  label: 'South',
                  backgroundColor: 'transparent',
                  borderColor: brandBlack,
                  pointHoverBackgroundColor: '#fff',
                  borderWidth: 2,
                  data: data4
              },
              {
                  label: 'Central',
                  backgroundColor: 'transparent',
                  borderColor: brandPrimary,
                  pointHoverBackgroundColor: '#fff',
                  borderWidth: 2,
                  data: data5
              }
              ]
            },
            options: {
                //   maintainAspectRatio: true,
                legend: {
                    display: true,
                    labels: {
                        fontColor: 'rgb(255, 99, 132)'
                    }
                },
                onAnimationComplete: function(){
                                      var url= myChart.toDataURL("image/png");
                                      document.getElementById("trafficChart").href=url;
                                    },
                // scales: {
                //     xAxes: [{
                //       display: false,
                //       categoryPercentage: 1,
                //       barPercentage: 0.5
                //     }],
                //     yAxes: [ {
                //         display: false
                //     } ]
                // }

                maintainAspectRatio: true,
                responsive: true,
                scales: {
                    xAxes: [{
                      gridLines: {
                        drawOnChartArea: true
                      }
                    }],
                    yAxes: [ {
                          ticks: {
                            beginAtZero: true,
                            maxTicksLimit: 5,
                            stepSize: Math.ceil(250 / 5),
                            max: 25
                          },
                          gridLines: {
                            display: true
                          }
                    } ]
                },
                elements: {
                    point: {
                      radius: 3,
                      hitRadius: 10,
                      hoverRadius: 4,
                      hoverBorderWidth: 3
                  }
              }


            }
        } );

//        var psiChart = document.getElementById('trafficChart').toDataURL('image/png');
//        document.getElementById('chart-download').href = psiChart;
    };

    //Dengue Chart
    function drawDengueChart(){
        console.log('Drawing Dengue Chart...');

        var ctx2 = document.getElementById( "dengueChart" ).getContext("2d");
        ctx2.height = 100;
        ctx2.width = 150;
        var myChart;
        var myChart;
        myChart = new Chart( ctx2, {
            type: 'line',
            data: {
                labels: generate_times(),
                datasets: [
                {
                  label: 'Last 2 Weeks',
                  backgroundColor: 'transparent',
                  borderColor: brandInfo,
                  pointHoverBackgroundColor: '#fff',
                  borderWidth: 2,
                  data: data6
              },
              {
                  label: 'Overall',
                  backgroundColor: 'transparent',
                  borderColor: brandSuccess,
                  pointHoverBackgroundColor: '#fff',
                  borderWidth: 2,
                  data: data7
              }
              ]
            },
            options: {
                //   maintainAspectRatio: true,
                //   legend: {
                //     display: false
                // },
                // scales: {
                //     xAxes: [{
                //       display: false,
                //       categoryPercentage: 1,
                //       barPercentage: 0.5
                //     }],
                //     yAxes: [ {
                //         display: false
                //     } ]
                // }
                onAnimationComplete: function(){
                                      var url= myChart.toDataURL("image/png");
                                      document.getElementById("trafficChart").href=url;
                                    },
                maintainAspectRatio: true,
                legend: {
                    display: true,
                    labels: {
                        fontColor: 'rgb(255, 99, 132)'
                    }
                },
                responsive: true,
                scales: {
                    xAxes: [{
                      gridLines: {
                        drawOnChartArea: true
                      }
                    }],
                    yAxes: [ {
                          ticks: {
                            beginAtZero: true,
                            maxTicksLimit: 5,
                            stepSize: Math.ceil(250 / 5),
                            max: 60
                          },
                          gridLines: {
                            display: true
                          }
                    } ]
                },
                elements: {
                    point: {
                      radius: 3,
                      hitRadius: 10,
                      hoverRadius: 4,
                      hoverBorderWidth: 3
                  }
              }


            }
        } );

//        var dengueChart = document.getElementById('trafficChart').toDataURL('image/png');
//        document.getElementById('chart-download').href = dengueChart;
    };

    drawPSIChart();
    drawDengueChart();
    console.log(document.getElementById( "dengueChart" ).style.width );
    document.getElementById( "trafficChart" ).style.width = "1050px";
    document.getElementById( "trafficChart" ).style.height = "375px";
    document.getElementById( "dengueChart" ).style.width = "1050px";
    document.getElementById( "dengueChart" ).style.height = "375px";
    console.log(document.getElementById( "dengueChart" ).style.width );

    function generate_times(){
        var current_time = new Date();
        var current_hours = current_time.getHours();
        var current_minutes = current_time.getMinutes();

        var times = [];
        if(0 <= current_minutes && current_minutes <= 9){
            current_minutes = "0" + current_minutes.toString();
        }
        times.push(current_hours + ":" + current_minutes);

        for(i=0; i<9; i++){
            current_minutes -= 30;
            if(current_minutes < 0){
                current_hours -= 1;
                current_minutes += 60;
            }
            if(0 <= current_minutes && current_minutes <= 9){
                current_minutes = "0" + current_minutes.toString();
            }
            times.push(current_hours + ":" + current_minutes);
        }

        return times.reverse();
    }