const selector = document.getElementById('status');
selector.addEventListener('change', (event) => {
    const possibleValues = new Array('appliedFor', 'accepted', 'completed');
    let index = possibleValues.findIndex(x => x === selector.value);
    $('.carousel').carousel(index);
});

$('.carousel').carousel('pause');


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
            console.log("made it");
            mapboxgl.accessToken = 'pk.eyJ1IjoieGFuZGVybSIsImEiOiJjbDFzc2t5aWUxcnl1M2ptdGZ6Y2c1emYxIn0.hBI_8hJfpKmssDHjOFB0aQ';
            console.log("made it here");
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