// Navbar scrolling configuration
window.addEventListener('DOMContentLoaded', () => {
    let scrollPos = 0;
    const mainNav = document.getElementById('mainNav');
    const headerHeight = mainNav.clientHeight;
    window.addEventListener('scroll', function() {
        const currentTop = document.body.getBoundingClientRect().top * -1;
        if ( currentTop < scrollPos) {
            // Scrolling Up
            if (currentTop > 0 && mainNav.classList.contains('is-fixed')) {
                mainNav.classList.add('is-visible');
            } else {
                console.log(123);
                mainNav.classList.remove('is-visible', 'is-fixed');
            }
        } else {
            // Scrolling Down
            mainNav.classList.remove(['is-visible']);
            if (currentTop > headerHeight && !mainNav.classList.contains('is-fixed')) {
                mainNav.classList.add('is-fixed');
            }
        }
        scrollPos = currentTop;
    });
});

// Change message submit button text
document.getElementById('contactForm').addEventListener('submit', function() {
   document.getElementById('submitButton').innerText = 'Sending...';
});

function incrementViews() {
    var viewsElement = document.getElementById('viewsCount');
    var currentViews = parseInt(viewsElement.innerText.split(':')[1].trim());
    var newViews = currentViews + 1;
    viewsElement.innerText = 'Views: ' + newViews;
  }

//function confirmDelete() {
//    if (confirm("Are you sure you want to delete your profile?")) {
//      window.location.href = "{{ url_for('delete_profile') }}";
//    } else {
//      // Ha a felhasználó nemmel vagy a felugró ablakot bezárja, nem történik semmi
//    }
//  }

// Confirm delete user profile confirmation
 function confirmDelete() {
    document.getElementById("confirmationModal").style.display = "block";
 }
 function hideConfirmation() {
    document.getElementById("confirmationModal").style.display = "none";
 }
 function deleteProfile() {
    window.location.href = "/delete_profile";
 }