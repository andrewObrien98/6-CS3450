const selector = document.getElementById('listings-type')

function hideAll() {
    const possibleValues = ['openListings', 'pendingListings', 'acceptedListings', 'completedListings'];
    for (let i = 0; i < 4; i++) {
        document.getElementById(possibleValues[i]).hidden = true;
    };
}

hideAll()
document.getElementById('openListings').hidden = false;

selector.addEventListener('change', (event) => {
    var selectorValue = selector.value;
    hideAll()
    document.getElementById(selectorValue).hidden = false;
});

