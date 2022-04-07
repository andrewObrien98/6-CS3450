const selector = document.getElementById('status');
selector.addEventListener('change', (event) => {
    const possibleValues = new Array('appliedFor', 'accepted', 'completed');
    let index = possibleValues.findIndex(x => x === selector.value);
    $('.carousel').carousel(index);
});

$('.carousel').carousel('pause');
