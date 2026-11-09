console.log("hello World")

// Local (docker compose) usa o backend em localhost:3001; publicado usa o backend no Render
const API_URL = ["localhost", "127.0.0.1"].includes(window.location.hostname)
    ? "http://localhost:3001"
    : "https://devops-backend-fnrq.onrender.com"

async function listar() {
    const res = await fetch(`${API_URL}/usuarios`)
    const dados = await res.json()

    console.log(dados)
    const table = document.getElementById("table1")
    if(dados.length!==0){
        
        table.innerHTML += dados.map(d => `
            <tr>
                <td>${d[1]}</td>
                <td>${d[2]}</td>
                <td>${d[3]}</td>
            </tr>
        `).join("")
    }
    else{
        table.innerHTML = "Houve um problema! Cheque se o banco tem registros, ou está ligado :P"
    }
    
}

listar()