// Get elements
const bookingModal = document.getElementById('bookingModal');
const bookNowBtn = document.getElementById('bookNowBtn');
const closeModal = document.getElementById('closeModal');
const bookingForm = document.getElementById('bookingForm');
const thankYouMessage = document.getElementById('thankYouMessage');

// Show the modal when 'Book Now' is clicked
bookNowBtn.onclick = function() {
    bookingModal.style.display = 'flex'; // Show the modal
    setTimeout(() => {
        bookingModal.classList.add('show'); // Trigger fade-in effect
        // Make modal content visible
        const modalContent = bookingModal.querySelector('.modal-content');
        modalContent.style.opacity = 1;
        modalContent.style.transform = 'translateY(0)';
    }, 10); // Small delay for CSS transition
}

// Close the modal when 'X' is clicked
closeModal.onclick = function() {
    const modalContent = bookingModal.querySelector('.modal-content');
    modalContent.style.opacity = 0; // Fade out effect
    modalContent.style.transform = 'translateY(100px)'; // Slide down
    bookingModal.classList.remove('show'); // Trigger fade-out effect
    setTimeout(() => {
        bookingModal.style.display = 'none'; // Hide the modal
    }, 400); // Match animation duration
}

// Hide modal when clicking outside the content
window.onclick = function(event) {
    if (event.target === bookingModal) {
        closeModal.onclick(); // Reuse close function
    }
}

// Function to get CSRF token for AJAX requests
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if this cookie string begins with the name we want
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Define the URL for the create_booking view at the start of your script
const createBookingUrl = "/create_booking/"; // Set this to your actual booking URL

// Form submission logic
bookingForm.onsubmit = function(event) {
    event.preventDefault(); // Prevent actual form submission

    // Gather form data
    const formData = new FormData(this);

    // Send form data to the Django backend
    fetch(createBookingUrl, {  // Use the defined URL here
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),  // Add CSRF token
        },
    })
    .then(response => {
        if (response.ok) {
            // Hide the form and show the thank you message
            bookingForm.style.display = 'none';
            thankYouMessage.style.display = 'block';
        } else {
            // Attempt to read the JSON error response
            return response.json().then(errorData => {
                alert(errorData.error || "There was an error with your booking. Please try again.");
            });
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
}
