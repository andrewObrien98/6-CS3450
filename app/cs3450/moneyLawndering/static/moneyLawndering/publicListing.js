let nums = document.getElementById("ul");
let listItem = nums.getElementsByTagName("li");

let newNums = [];

for (var i=0; i < listItem.length; i++) {
    newNums.push( listItem[i].id );
}

for (let listingNum = 0; listingNum < newNums.length; listingNum++) {
    let locationID = "location" + (listingNum + 1);
    let location = document.getElementById(locationID).innerHTML;

    let userAddress = encodeURI(location);
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
            let randNum1 = Math.floor(Math.random() * 5) / 1000; // Randomize the map location so the person won't know exact address within +/- .3 miles
            let randNum2 = Math.floor(Math.random() * 5) / 1000;
            long += randNum1;
            latit += randNum2;
            mapboxgl.accessToken = 'pk.eyJ1IjoieGFuZGVybSIsImEiOiJjbDFzc2t5aWUxcnl1M2ptdGZ6Y2c1emYxIn0.hBI_8hJfpKmssDHjOFB0aQ';
            const map = new mapboxgl.Map({
                container: `map${listingNum + 1}`, // Container ID
                style: 'mapbox://styles/mapbox/streets-v11', // Map style to use
                center: [latit, long], // Starting position [lng, lat]
                zoom: 15, // Starting zoom level
            });
            let marker = new mapboxgl.Marker();
            marker.setLngLat([latit, long]);
            marker.addTo(map);
        }
    })
    .catch(err => {
        console.log(`Error!: ${json.error}`);
    })
}