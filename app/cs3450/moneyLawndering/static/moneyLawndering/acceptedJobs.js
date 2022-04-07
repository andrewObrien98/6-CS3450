const selector = document.getElementById('status')

function hideAll() {
    const possibleValues = ['appliedFor', 'accepted', 'completed'];
    for (let i = 0; i < 3; i++) {
        document.getElementById(possibleValues[i]).hidden = true;
    };
}

hideAll()
// Set selector value to match initial section being shown
selector.value = 'accepted';
document.getElementById('accepted').hidden = false;

selector.addEventListener('change', (event) => {
    var selectorValue = selector.value;
    hideAll()
    document.getElementById(selectorValue).hidden = false;
});

