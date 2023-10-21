document.addEventListener('DOMContentLoaded', function() {
  var logoutLink = document.getElementById('logout-link');
  var logoutPopup = document.getElementById('logout-popup');
  var logoutBtn = document.getElementById('logout-btn');
  
  var showPopup = function() {
    logoutPopup.style.display = 'block';
  };

  var hidePopup = function() {
    logoutPopup.style.display = 'none';
  };

  logoutLink.addEventListener('mouseenter', showPopup);
  logoutLink.addEventListener('mouseleave', hidePopup);
  logoutPopup.addEventListener('mouseenter', showPopup);
  logoutPopup.addEventListener('mouseleave', hidePopup);

  logoutBtn.addEventListener('click', function(e) {
    e.preventDefault();
    window.location.href = "/logout";
  });
});
