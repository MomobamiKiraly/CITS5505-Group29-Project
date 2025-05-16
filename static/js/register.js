let current = 0;
const steps = document.querySelectorAll('.step');

// Go to next step in registration
function nextStep() {
  if (current < steps.length - 1) {
    steps[current].classList.remove('active');
    current++;
    steps[current].classList.add('active');
  }
}

// Go to previous step in registration
function prevStep() {
  if (current > 0) {
    steps[current].classList.remove('active');
    current--;
    steps[current].classList.add('active');
  }
}

// Log form submission
document.querySelector('form').addEventListener('submit', (e) => {
  console.log("Form submitted.");
});

// Select a team and show drivers for that team
function selectTeam(el) {
  document.querySelectorAll('.team').forEach(e => e.classList.remove('selected'));
  el.classList.add('selected');

  const teamName = el.dataset.value;
  document.getElementById('favorite_team').value = teamName;

  const driverSection = document.getElementById('driverSection');
  const driverContainer = document.getElementById('driverContainer');
  driverSection.style.display = 'block';
  driverContainer.innerHTML = '';

  if (driversByTeam[teamName]) {
    driversByTeam[teamName].forEach(driver => {
      const div = document.createElement('div');
      div.className = 'driver';
      div.setAttribute('data-value', driver.name);

      const img = document.createElement('img');
      img.src = driver.image_url;
      img.alt = driver.name;

      const label = document.createElement('p');
      label.innerText = driver.name;

      div.appendChild(img);
      div.appendChild(label);
      driverContainer.appendChild(div);

      // Select a driver
      div.onclick = function () {
        document.querySelectorAll('.driver').forEach(d => d.classList.remove('selected'));
        div.classList.add('selected');
        document.getElementById('favorite_driver').value = driver.name;
      };
    });
  }
}
