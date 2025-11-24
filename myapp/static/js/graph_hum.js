fetch("/api")
    .then(res => res.json())
    .then(json => {
        const data = json.data;

        const labels = data.map(d => new Date(d.dt).toLocaleTimeString());
        const values = data.map(d => d.hum);

        new Chart(document.getElementById("humChart"), {
            type: "line",
            data: {
                labels: labels,
                datasets: [{
                    label: "Humidité (%)",
                    data: values,
                    borderWidth: 2
                }]
            }
        });
    });
