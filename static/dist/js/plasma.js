var x = document.getElementById("demo");
var mapBtn = document.getElementById("mapButton1")
var locBtn = document.getElementById("locateButton1")
var infTxt = document.getElementById("infoText")
var user_latitude = 0;
var user_longitude = 0;
var plotData = ""
var markers = []
var hospital = ""

function getLocation() {
  if (navigator.geolocation) {
    infTxt.style.visibility = "visible";
    navigator.geolocation.getCurrentPosition(showPosition);
  } else {
    x.innerHTML = "Geolocation is not supported by this browser.";
  }
}

function showPosition(position) {
  user_latitude = position.coords.latitude;
  user_longitude = position.coords.longitude;
  console.log(user_latitude, user_longitude)
  sendData()
}

function sendData(){
    axios.post("http://127.0.0.1:500/plsdata",{
        latitude: user_latitude,
        longitude: user_longitude
    }).then(response => {
        plotData = response.data;
        infTxt.style.visibility = "hidden";
    });
}

function initMap(){

      var options = {
        zoom:9,
        center:{lat:user_latitude,lng:user_longitude}
      }

      console.log(options)

      var map = new google.maps.Map(document.getElementById('map'), options);


      for (const item in plotData){
        var hospital = plotData[item]["binfo"]
        var address = plotData[item]["address"]
        var bed1 = plotData[item]["beds"]
        var la = parseFloat(plotData[item]["latitude"])
        var lo = parseFloat(plotData[item]["longitude"])
        markers.push({
          coords:{lat:la,lng:lo},
          iconImage:'http://127.0.0.1:500/static/images/hospital.png',
          content:'<h3>'+hospital+'</h3><br><p>'+address+'</p><br><b>'+bed1+'</b>'
        })
      }
      if(true)
        {
          var userlat = parseFloat(user_latitude)
          var userlong = parseFloat(user_longitude)
          markers.push({
            coords:{lat:userlat,lng:userlong},
            iconImage:'http://127.0.0.1:500/static/images/userpin.png',
            content:'<h3>'+'Saud'+'</h3><br><p>'+'Malad, Malwani'+'</p>'
          })
          // Add circle overlay and bind to marker
          var circle = new google.maps.Circle({
            map: map,
            center: { lat: user_latitude, lng: user_longitude},
            radius: 2000,    // 10 miles in metres
            strokeColor: "##FF4A4A",
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: "#FFC7C7",
            fillOpacity: 0.35,
          });
          //circle.bindTo('center', markers, '19.1826682,72.81608609999999);
        }

      console.log(markers)
      for(var i = 0;i < markers.length;i++){
        addMarker(markers[i]);
      }


      function addMarker(props){
        var marker = new google.maps.Marker({
          position:props.coords,
          map:map,
          icon:props.iconImage
        });


          var infoWindow = new google.maps.InfoWindow({
            content:props.content
          });

          marker.addListener('click', function(){
            infoWindow.open(map, marker);
          });

      }
    }

