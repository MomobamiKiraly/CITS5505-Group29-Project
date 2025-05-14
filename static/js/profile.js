document.addEventListener("DOMContentLoaded", function () {
    showSection('blog');  // default

    const checkbox = document.getElementById("is_public");
    if (checkbox) {
        checkbox.addEventListener("change", function () {
            console.log("Post visibility set to:", checkbox.checked ? "Public" : "Followers only");
        });
    }
});

function showSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('.section-tab').forEach(sec => {
        sec.classList.remove('active');
    });

    // Show selected section
    const selected = document.getElementById(sectionId);
    if (selected) selected.classList.add('active');

    // Update button state
    document.querySelectorAll('.toggle-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.getAttribute('onclick').includes(sectionId)) {
            btn.classList.add('active');
        }
    });
}
