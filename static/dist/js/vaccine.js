function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  }
}

function showPosition(position) {
  user_latitude = position.coords.latitude;
  user_longitude = position.coords.longitude;
  console.log(user_latitude, user_longitude)
 // x.innerHTML = "Latitude: " + position.coords.latitude + "<br>Longitude: " + position.coords.longitude;
//  x.innerHTML = "Latitude: " + user_latitude + "<br>Longitude: " + user_longitude;
  sendData()
}

function sendData(){
    axios.post("http://127.0.0.1:500/saveDataForVaccine",{
        latitude: user_latitude,
        longitude: user_longitude
    }).then(response => {
        plotData = response.data;
    });
}