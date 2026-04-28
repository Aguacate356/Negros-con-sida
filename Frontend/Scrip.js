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

const PYTHON_EXE  = "C:\\Users\\q\\AppData\\Local\\Programs\\Python\\Python314\\python.exe";
const SCRIPT_PATH = "C:\\Users\\q\\Desktop\\Simulación_Python\\PrediccionGasolina.py";

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

function estimar() {
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

    const cmd = `"${PYTHON_EXE}" "${SCRIPT_PATH}" ${id} ${year} ${mes} ${tipoGas}`;
    document.getElementById("cmdText").textContent = cmd;
    document.getElementById("resultInfo").textContent =
    `Municipio: ${municipio}  ·  Gasolina: ${tipoGas}  ·  Mes ${mes}, ${year}`;
    document.getElementById("p5").textContent  = "—";
    document.getElementById("p50").textContent = "—";
    document.getElementById("p95").textContent = "—";
    document.getElementById("resultCard").style.display = "block";
}

function copiarCmd() {
    navigator.clipboard.writeText(document.getElementById("cmdText").textContent).catch(() => {});
    const btn = document.querySelector(".est-copy-btn");
    btn.textContent = "¡Copiado!";
    setTimeout(() => btn.textContent = "Copiar comando", 2000);
}