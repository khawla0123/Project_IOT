// dashboard.js – VERSION FINALE QUI MARCHE À TOUS LES COUPS

document.addEventListener("DOMContentLoaded", function () {

    function majDashboard() {
        fetch('/latest_json/')
            .then(response => response.json())
            .then(d => {
                if (d.temp !== '--') {
                    // Valeurs
                    document.getElementById('temp').textContent = Number(d.temp).toFixed(1);
                    document.getElementById('hum').textContent = Number(d.hum).toFixed(1);

                    // Temps écoulé en minutes
                    const dateMesure = new Date(d.dt);
                    const maintenant = new Date();
                    const diffMinutes = Math.floor((maintenant - dateMesure) / 1000 / 60);

                    let texte = "";
                    if (diffMinutes < 1) texte = "moins d'1 minute";
                    else if (diffMinutes === 1) texte = "1 minute";
                    else if (diffMinutes < 60) texte = diffMinutes + " minutes";
                    else {
                        const h = Math.floor(diffMinutes / 60);
                        const m = diffMinutes % 60;
                        texte = h + " h" + (m > 0 ? " " + m + " min" : "");
                    }

                    // Mise à jour des DEUX cartes (même id)
                    document.querySelectorAll('#temps-ecoule').forEach(el => {
                        el.textContent = texte;
                    });
                }
            })
            .catch(err => console.error("Erreur AJAX :", err));
    }

    // Lancement immédiat + toutes les 20 minutes
    majDashboard();
    setInterval(majDashboard, 20 * 60 * 1000);  // 20 minutes
});