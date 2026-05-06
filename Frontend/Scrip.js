const IDGasolinera = {
    "Apodaca":          ["2"],
    "Aramberri":        ["10"],
    "Galeana":          ["8"],
    "Garcia":           ["6"],
    "General Escobedo": ["9"],
    "Guadalupe":        ["3"],
    "Juarez":           ["4"],
    "Montemorelos":     ["7"],
    "Monterrey":        ["1"],
    "Santa Catarina":   ["5"]
};
 
function updateID() {
    const mun = document.getElementById("municipio").value;
    const sel = document.getElementById("idGas");
    sel.innerHTML = "";
    if (IDGasolinera[mun]) {
        IDGasolinera[mun].forEach(id => {
            const opt = document.createElement("option");
            opt.value = id; opt.textContent = id;
            sel.appendChild(opt);
        });
        sel.disabled = false;
    } else {
        sel.innerHTML = '<option value="">—</option>';
        sel.disabled = true;
    }
}
 
function showErr(msg) {
    const el = document.getElementById("errMsg");
    el.textContent = msg;
    el.style.display = msg ? "block" : "none";
}
 
async function estimar() {
    showErr("");
    const municipio = document.getElementById("municipio").value;
    const id        = document.getElementById("idGas").value;
    const tipoGas   = document.getElementById("tipoGas").value;
    const mes       = document.getElementById("mes").value;
    const year      = document.getElementById("year").value;
 
    if (!municipio) return showErr("Por favor, selecciona un municipio.");
    if (!tipoGas)   return showErr("Por favor, selecciona un tipo de gasolina.");
    if (!mes)       return showErr("Por favor, selecciona un mes.");
    if (!year)      return showErr("Por favor, selecciona un año.");
 
    document.getElementById("resultInfo").textContent =
        `Municipio: ${municipio}  ·  Gasolina: ${tipoGas}  ·  Mes ${mes}, ${year}`;
    document.getElementById("p5").textContent  = "...";
    document.getElementById("p50").textContent = "...";
    document.getElementById("p95").textContent = "...";
    document.getElementById("resultCard").style.display = "block";
 
    const btn = document.querySelector(".est-btn");
    btn.textContent = "Calculando...";
    btn.disabled = true;
 
    try {
        // appSimulacion.py recibe: id_gas, ano, mes, tipo
        const url = `http://localhost:5001/getUserData?id_gas=${id}&ano=${year}&mes=${mes}&tipo=${tipoGas}`;
        const resp = await fetch(url);
        const data = await resp.json();
 
        if (!resp.ok) {
            showErr("Error del servidor: " + (data.error || resp.status));
            document.getElementById("p5").textContent  = "—";
            document.getElementById("p50").textContent = "—";
            document.getElementById("p95").textContent = "—";
            return;
        }
 
        document.getElementById("p5").textContent  = "$" + parseFloat(data.p5).toFixed(2);
        document.getElementById("p50").textContent = "$" + parseFloat(data.p50).toFixed(2);
        document.getElementById("p95").textContent = "$" + parseFloat(data.p95).toFixed(2);
 
    } catch (e) {
        showErr("No se pudo conectar al servidor. ¿Está corriendo appSimulacion.py?");
        document.getElementById("p5").textContent  = "—";
        document.getElementById("p50").textContent = "—";
        document.getElementById("p95").textContent = "—";
    } finally {
        btn.textContent = "Estimar precio";
        btn.disabled = false;
    }
}
 

 