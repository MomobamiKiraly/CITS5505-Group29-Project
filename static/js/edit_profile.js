document.addEventListener('DOMContentLoaded', function () {
    const teamSelect = document.getElementById('favorite_team');
    const driverSelect = document.getElementById('favorite_driver');

    function populateDrivers(teamName) {
        const drivers = driversByTeam[teamName] || [];
        driverSelect.innerHTML = '';

        drivers.forEach(driver => {
            const option = document.createElement('option');
            option.value = driver.name;
            option.textContent = driver.name;
            driverSelect.appendChild(option);
        });
    }

    teamSelect.addEventListener('change', function () {
        populateDrivers(this.value);
    });

    if (teamSelect.value) {
        populateDrivers(teamSelect.value);
    }
});
