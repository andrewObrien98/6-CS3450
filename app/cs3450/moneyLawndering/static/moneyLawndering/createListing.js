const locationElement = document.getElementById('location');

var map;
var marker;

let userAddress = encodeURI(locationElement.value);
let URL = `https://api.mapbox.com/geocoding/v5/mapbox.places/${userAddress}.json?access_token=pk.eyJ1IjoieGFuZGVybSIsImEiOiJjbDFzc2t5aWUxcnl1M2ptdGZ6Y2c1emYxIn0.hBI_8hJfpKmssDHjOFB0aQ`;
fetch(URL)
.then(response => {
    console.log(`The HTTP status code is ${response.status}`);
    return response.json()
})
.then(json => {
    if (json.hasOwnProperty('error')) {
        console.log(`Error!: ${json.error}`);
    }
    else {
        let long = json.features[0].geometry.coordinates[1];
        let latit = json.features[0].geometry.coordinates[0];
        mapboxgl.accessToken = 'pk.eyJ1IjoieGFuZGVybSIsImEiOiJjbDFzc2t5aWUxcnl1M2ptdGZ6Y2c1emYxIn0.hBI_8hJfpKmssDHjOFB0aQ';
            map = new mapboxgl.Map({
            container: 'map', // Container ID
            style: 'mapbox://styles/mapbox/streets-v11', // Map style to use
            center: [latit, long], // Starting position [lng, lat]
            zoom: 15, // Starting zoom level
        });
        marker = new mapboxgl.Marker();
        marker.setLngLat([latit, long]);
        marker.addTo(map);
    }
})
.catch(err => {
    console.log(`Error!: ${json.error}`);
})

locationElement.addEventListener('change', (event) => {
    let locationText = encodeURI(locationElement.value);
    let URL = `https://api.mapbox.com/geocoding/v5/mapbox.places/${locationText}.json?access_token=pk.eyJ1IjoieGFuZGVybSIsImEiOiJjbDFzc2t5aWUxcnl1M2ptdGZ6Y2c1emYxIn0.hBI_8hJfpKmssDHjOFB0aQ`;
    fetch(URL)
    .then(response => {
        console.log(`The HTTP status code is ${response.status}`);
        return response.json()
    })
    .then(json => {
        if (json.hasOwnProperty('error')) {
            console.log(`Error!: ${json.error}`);
        }
        else {
            let long1 = json.features[0].geometry.coordinates[1];
            let latit1 = json.features[0].geometry.coordinates[0];
            map.flyTo({
                center: [latit1, long1],
                zoom: 16,
            });
            marker.setLngLat([latit1, long1]);
        }
    })
    .catch(err => {
        console.log(`Error!: ${json.error}`);
    })
});

