console.log("dashboard.js loaded");

document.addEventListener("DOMContentLoaded", async () => {
  console.log("DOM Loaded");

  // -------------------------
  // Grade Distribution
  // -------------------------

  const gradeCanvas = document.getElementById("gradeChart");

  if (gradeCanvas) {
    const response = await fetch("/api/dashboard/grade-distribution");

    const gradeData = await response.json();

    new Chart(gradeCanvas, {
      type: "pie",

      data: {
        labels: Object.keys(gradeData),

        datasets: [
          {
            data: Object.values(gradeData),
          },
        ],
      },
    });
  }

  // -------------------------
  // Subject Performance
  // -------------------------

  const subjectCanvas = document.getElementById("subjectChart");

  if (subjectCanvas) {
    const response = await fetch("/api/dashboard/subject-statistics");

    const data = await response.json();

    new Chart(subjectCanvas, {
      type: "bar",

      data: {
        labels: data.map((item) => item.subject),

        datasets: [
          {
            label: "Average Marks",

            data: data.map((item) => item.average),
          },
        ],
      },

      options: {
        responsive: true,
        maintainAspectRatio: true,

        scales: {
          y: {
            beginAtZero: true,

            max: 100,
          },
        },
      },
    });
  }
});
