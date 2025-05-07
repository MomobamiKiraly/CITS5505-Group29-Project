
document.addEventListener("DOMContentLoaded", function () {
    const checkbox = document.getElementById("is_public");
    if (checkbox) {
        checkbox.addEventListener("change", function () {
            console.log("Post visibility set to:", checkbox.checked ? "Public" : "Followers only");
        });
    }
});
