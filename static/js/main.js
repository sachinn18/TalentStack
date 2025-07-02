document.addEventListener('DOMContentLoaded', function() {
    const deleteForms = document.querySelectorAll('.confirm-delete');
    
    deleteForms.forEach(form => {
        form.addEventListener('submit', function(event) {
            const confirmation = confirm('Are you sure you want to delete this item? This action cannot be undone.');
            if (!confirmation) {
                event.preventDefault();
            }
        });
    });
});

// Handle smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Add scroll-based navbar background
window.addEventListener('scroll', function() {
    const header = document.querySelector('.main-header');
    if (window.scrollY > 50) {
        header.style.background = 'rgba(255, 255, 255, 0.95)';
    } else {
        header.style.background = 'rgba(255, 255, 255, 0.9)';
    }
});

// Initialize any carousels or sliders
if (document.querySelector('.swiper')) {
    new Swiper('.swiper', {
        slidesPerView: 1,
        spaceBetween: 30,
        loop: true,
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        breakpoints: {
            640: {
                slidesPerView: 2,
            },
            968: {
                slidesPerView: 3,
            }
        }
    });
}

// Add loading animations
window.addEventListener('load', function() {
    document.body.classList.add('loaded');
});

// Handle form submissions with loading states
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function() {
        const submitButton = this.querySelector('[type="submit"]');
        if (submitButton) {
            submitButton.disabled = true;
            submitButton.innerHTML = '<i class="bi bi-hourglass-split"></i> Processing...';
        }
    });
});

// Job search functionality
document.addEventListener('DOMContentLoaded', function() {
    const searchButton = document.querySelector('.search-box .btn-primary');
    const jobSearchInput = document.getElementById('jobSearch');
    const locationSearchInput = document.getElementById('locationSearch');

    searchButton.addEventListener('click', function() {
        const jobQuery = jobSearchInput.value.trim();
        const locationQuery = locationSearchInput.value.trim();
        
        // Construct the search URL
        const searchParams = new URLSearchParams();
        if (jobQuery) searchParams.append('job', jobQuery);
        if (locationQuery) searchParams.append('location', locationQuery);
        
        // Redirect to the search results
        window.location.href = `/search?${searchParams.toString()}`;
    });

    // Enable search on Enter key
    [jobSearchInput, locationSearchInput].forEach(input => {
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                searchButton.click();
            }
        });
    });
});