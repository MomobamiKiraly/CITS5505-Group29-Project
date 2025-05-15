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
      if (driver.name === selectedDriver) {
        option.selected = true;
      }
      driverSelect.appendChild(option);
    });
  }

  
  if (selectedTeam) {
    populateDrivers(selectedTeam);
  }

  
  teamSelect.addEventListener('change', function () {
    populateDrivers(this.value);
  });
});
