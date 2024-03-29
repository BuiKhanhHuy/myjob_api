let loadingOverlay = document.createElement('div');
loadingOverlay.className = 'loading-overlay';
loadingOverlay.innerHTML = '<div class="loading-spinner"></div>';

function showLoadingOverlay() {
  document.body.appendChild(loadingOverlay);
}

function hideLoadingOverlay() {
  document.body.removeChild(loadingOverlay);
}

var links = document.querySelectorAll('a');

for (var i = 0; i < links.length; i++) {
  var link = links[i];
  link.addEventListener('click', function(event) {
    event.preventDefault();
    showLoadingOverlay();
    window.location.href = this.href;
  });
}

window.addEventListener('beforeunload', function() {
  showLoadingOverlay();
});

window.addEventListener('load', function() {
  hideLoadingOverlay();
});