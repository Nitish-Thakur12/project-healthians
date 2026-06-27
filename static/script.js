const symptomInput = document.getElementById("symptoms");
const analyzeBtn = document.getElementById("analyzeBtn");
const conditionsEl = document.getElementById("conditions");
const recommendationsEl = document.getElementById("recommendations");
const severityEl = document.getElementById("severity");
const medicalEl = document.getElementById("medicalAttention");
const historyList = document.getElementById("historyList");

// Form click tagging integration
document.querySelectorAll(".tag").forEach(tag => {
    tag.addEventListener("click", () => {
        const value = tag.textContent.trim();
        if (symptomInput.value.trim() === "") {
            symptomInput.value = value;
        } else if (!symptomInput.value.includes(value)) {
            symptomInput.value += ", " + value;
        }
    });
});

// Async network routing requests to Flask
analyzeBtn.addEventListener("click", async () => {
    const symptoms = symptomInput.value.trim();
    if (!symptoms) {
        alert("Please explain your symptoms before running analysis.");
        return;
    }

    try {
        const response = await fetch("/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ symptoms: symptoms })
        });

        if (!response.ok) throw new Error("Backend parsing error encountered.");
        const data = await response.json();

        // Flush previous lists clean
        conditionsEl.innerHTML = "";
        recommendationsEl.innerHTML = "";
        medicalEl.innerHTML = "";

        // Build elegant structural visual blocks dynamically
        data.results.forEach(item => {
            conditionsEl.innerHTML += `<div class="result-item"><strong>${item.condition}</strong></div>`;
            recommendationsEl.innerHTML += `<div class="result-item">${item.recommendation}</div>`;
            medicalEl.innerHTML += `<div class="result-item">${item.medical_attention}</div>`;
        });

        // Set up severity level tags
        severityEl.textContent = data.severity;
        severityEl.className = "severity-pill";
        severityEl.classList.add(`severity-${data.severity.toLowerCase()}`);

        saveHistory(symptoms);
    } catch (error) {
        console.error(error);
        alert("Communications mismatch with Flask. Verify terminal python tracking context.");
    }
});

function saveHistory(text) {
    let history = JSON.parse(localStorage.getItem("symptomHistory")) || [];
    history = history.filter(item => item.toLowerCase() !== text.toLowerCase());
    history.unshift(text);
    history = history.slice(0, 4);
    localStorage.setItem("symptomHistory", JSON.stringify(history));
    loadHistory();
}

function loadHistory() {
    let history = JSON.parse(localStorage.getItem("symptomHistory")) || [];
    historyList.innerHTML = "";
    history.forEach(item => {
        const li = document.createElement("li");
        li.textContent = item.length > 40 ? item.substring(0, 37) + "..." : item;
        li.addEventListener("click", () => { symptomInput.value = item; });
        historyList.appendChild(li);
    });
}

// Light & Dark Theme Configuration state checks
const themeBtn = document.getElementById("themeToggle");
if (themeBtn) {
    themeBtn.addEventListener("click", () => {
        document.body.classList.toggle("dark-mode");
        localStorage.setItem("darkTheme", document.body.classList.contains("dark-mode"));
    });
}
if (localStorage.getItem("darkTheme") === "true") {
    document.body.classList.add("dark-mode");
}

loadHistory();