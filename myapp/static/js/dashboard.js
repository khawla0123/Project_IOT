const API_URL = "/latest_json/";  // l'URL Django pour récupérer la dernière donnée

async function loadData() {
    try {
        const res = await fetch(API_URL);   // <--- ici on appelle l'API Django
        const data = await res.json();       // on récupère la réponse JSON

        document.getElementById("temp").textContent = data.temp + " °C";
        document.getElementById("hum").textContent  = data.hum + " %";

        const time = data.dt !== "--" ? new Date(data.dt).toLocaleTimeString() : "--";
        document.getElementById("time_temp").textContent = time;
        document.getElementById("time_hum").textContent = time;

        document.getElementById("status").textContent = "Mise à jour OK";
    } catch (err) {
        document.getElementById("status").textContent = "Erreur : " + err;
    }
}

// charger au démarrage et toutes les 5 secondes
loadData();
setInterval(loadData, 5000);
