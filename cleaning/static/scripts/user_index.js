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

// // Define the URL for the create_booking view at the start of your script
 const createBookingUrl = "/create_booking/"; // Set this to your actual booking URL

// Form submission logic
// bookingForm.onsubmit = function(event) {
    // event.preventDefault(); // Prevent actual form submission

    // Gather form data
    // const formData = new FormData(this);

    // Send form data to the Django backend
    // fetch("/booking/create/", {  // Use the correct URL path here
    //     method: "POST",
    //     body: formData,
    //     headers: {
    //         "X-CSRFToken": getCookie('csrftoken'),
    //     },
        
    // })
    // .then(response => {
    //     if (response.ok) {
    //         // Hide the form and show the thank you message
    //         bookingForm.style.display = 'none';
    //         thankYouMessage.style.display = 'block';
    //     } else {
    //         alert("There was an error with your booking. Please try again.");
    //     }
    // })
    // .catch(error => {
    //     console.error("Error:", error);
    // });
$(document).ready(function(){
    $('#booking_submit_btn').on('click', function(){
        create_booking($(this));
    })


    function create_booking(btn){
        let form = $(btn).closest('#bookingForm');
        console.log(form);
        form_data = {
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken').val(),
            'cleaning_service': form.find('select[name="cleaning_service"]').val(),
            'first_name': form.find('input[name="first_name"]').val(),
            'last_name': form.find('input[name="last_name"]').val(),
            'contact_number': form.find('input[name="contact_number"]').val(),
            'address': form.find('textarea[name="address"]').val(),
            'additional_info': form.find('textarea[name="additional_info"]').val(),
        }
        console.log(form_data);
        alert(form_data);
        $.ajax({
            url: '/booking_create/views/',
            type: 'POST',
            data: form_data,
            success: function(){
                alert('SUCCESS');
            },
            error: function(xhr, status, error){
                if(xhr.responseJSON && xhr.responseJSON.error){
                    alert(`Error ${xhr.status}: ${xhr.responseJSON.error}`);
                } else {
                    alert(`Error ${xhr.status}: ${error}`);
                }
            }
        })
    }
});// jquery end
  // Toggle Sidebar
  function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    sidebar.style.width = sidebar.style.width === "250px" ? "0" : "250px";
}

// Toggle Modal
function toggleModal() {
    const modal = document.getElementById("bookingModal");
    modal.style.display = modal.style.display === "block" ? "none" : "block";
}

// Close Modal when clicking the 'x' or outside of the modal
document.getElementById("closeModal").onclick = function() {
    toggleModal();
}

window.onclick = function(event) {
    const modal = document.getElementById("bookingModal");
    if (event.target === modal) {
        modal.style.display = "none";
    }
}

// Form Submission
document.getElementById("bookingForm").onsubmit = function(event) {
    event.preventDefault(); // Prevent form from submitting traditionally
    const thankYouMessage = document.getElementById("thankYouMessage");
    thankYouMessage.style.display = "block";
    setTimeout(() => {
        thankYouMessage.style.display = "none";
        toggleModal(); // Close modal after showing thank you message
    }, 3000); // Hide message after 3 seconds
}

// Book Now button opens the modal
document.getElementById("bookNowBtn").onclick = function() {
    toggleModal();
}
