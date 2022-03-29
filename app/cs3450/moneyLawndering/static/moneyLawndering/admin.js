const selector = document.getElementById('model-type');

// Hide listings as the default
document.getElementById('listings').hidden = true;

// Create an event listener to update what is visible based on table chosen in selector
selector.addEventListener('change', (event) => {
    var selectorValue = selector.value;
    if (selectorValue == 'users') {
        document.getElementById(selectorValue).hidden = false;
        document.getElementById('listings').hidden = true;
    } else {
        document.getElementById(selectorValue).hidden = false;
        document.getElementById('users').hidden = true;
    }
});


