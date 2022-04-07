const selector = document.getElementById('listings-type');
selector.addEventListener('change', (event) => {
    const possibleValues = new Array('openListings', 'pendingListings', 'acceptedListings', 'completedListings');
    let index = possibleValues.findIndex(x => x === selector.value);
    $('.carousel').carousel(index);
});

$('.carousel').carousel('pause');
