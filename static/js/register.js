let current = 0;
const steps = document.querySelectorAll('.step');

// Handle multi-step logic
function nextStep() {
    if (current < steps.length - 1) {
        steps[current].classList.remove('active');
        current++;
        steps[current].classList.add('active');
    }
}

function prevStep() {
    if (current > 0) {
        steps[current].classList.remove('active');
        current--;
        steps[current].classList.add('active');
    }
}

// 🚨 Moved outside selectTeam — runs on load!
document.querySelector('form').addEventListener('submit', (e) => {
    console.log("Form submitting...");
    console.log("teamInput value:", document.getElementById('teamInput').value);
    console.log("driverInput value:", document.getElementById('driverInput').value);
});

// Team selection logic
function selectTeam(el) {
    document.querySelectorAll('.team').forEach(e => e.classList.remove('selected'));
    el.classList.add('selected');

    const teamName = el.dataset.value;
    console.log("Selected team:", teamName);
    document.getElementById('favorite_team').value = teamName;

    document.getElementById('driverSection').style.display = 'block';
    const driverContainer = document.getElementById('driverContainer');
    driverContainer.innerHTML = '';

    if (driversByTeam[teamName]) {
        driversByTeam[teamName].forEach(driver => {
            const div = document.createElement('div');
            div.className = 'driver';

            const img = document.createElement('img');
            img.src = driver.image_url;
            img.alt = driver.name;
            img.setAttribute('data-value', driver.name);

            img.onclick = function () {
                document.querySelectorAll('.driver').forEach(d => d.classList.remove('selected'));
                div.classList.add('selected');
                document.getElementById('favorite_driver').value = driver.name;
                console.log("Selected driver:", driver.name);
            };

            const label = document.createElement('p');
            label.innerText = driver.name;
            label.style.color = 'white';
            label.style.fontSize = '0.9rem';

            div.appendChild(img);
            div.appendChild(label);
            driverContainer.appendChild(div);
        });
    }
}
