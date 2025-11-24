fetch("/api")
    .then(res => res.json())
    .then(json => {
        const data = json.data;

        const labels = data.map(d => new Date(d.dt).toLocaleTimeString());
        const values = data.map(d => d.temp);

        new Chart(document.getElementById("tempChart"), {
            type: "line",
            data: {
                labels: labels,
                datasets: [{
                    label: "Température (°C)",
                    data: values,
                    borderWidth: 2
                }]
            }
        });
    });
