document.addEventListener('DOMContentLoaded', function () {
  const teamSelect = document.getElementById('favorite_team');
  const driverSelect = document.getElementById('favorite_driver');

  // Populate driver options based on selected team
  function populateDrivers(teamName) {
    const drivers = driversByTeam[teamName] || [];
    driverSelect.innerHTML = '';

    drivers.forEach(driver => {
      const option = document.createElement('option');
      option.value = driver.name;
      option.textContent = driver.name;
      if (driver.name === selectedDriver) {
        option.selected = true;
      }
      driverSelect.appendChild(option);
    });
  }

  // If a team is already selected, populate drivers
  if (selectedTeam) {
    populateDrivers(selectedTeam);
  }

  // Update drivers when team selection changes
  teamSelect.addEventListener('change', function () {
    populateDrivers(this.value);
  });
});
