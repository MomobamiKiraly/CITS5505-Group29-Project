document.addEventListener("DOMContentLoaded", () => {
  const canvas = document.getElementById("standingsChart");
  if (!canvas) return;

  const ctx = canvas.getContext("2d");
  if (!ctx || !driverNames || !driverPoints) return;

  // Render bar chart for top 5 F1 drivers
  new Chart(ctx, {
    type: "bar",
    data: {
      labels: driverNames,
      datasets: [{
        label: "Points",
        data: driverPoints,
        backgroundColor: [
          "rgba(255, 99, 132, 0.8)",
          "rgba(255, 159, 64, 0.8)",
          "rgba(54, 162, 235, 0.8)",
          "rgba(75, 192, 192, 0.8)",
          "rgba(153, 102, 255, 0.8)"
        ],
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        title: {
          display: true,
          text: "Top 5 F1 Drivers — 2025 Standings",
          color: "white"
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: { color: "white" },
          grid: { color: "rgba(255,255,255,0.1)" }
        },
        x: {
          ticks: { color: "white" },
          grid: { color: "rgba(255,255,255,0.1)" }
        }
      }
    }
  });
});