document.addEventListener('DOMContentLoaded', function() {
    var toggles = document.getElementsByClassName('toggle');

    for (var i = 0; i < toggles.length; i++) {
        toggles[i].addEventListener('click', function() {
            var content = this.nextElementSibling;
            if (content.style.display === 'none') {
                content.style.display = 'block';
            } else {
                content.style.display = 'none';
            }
        });
    }
});
