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

// Form submission logic
bookingForm.onsubmit = function(event) {
    event.preventDefault(); // Prevent actual form submission

    // Hide form and show thank you message
    bookingForm.style.display = 'none';
    thankYouMessage.style.display = 'block';
}
