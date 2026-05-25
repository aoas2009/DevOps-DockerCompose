console.log("hello World")

async function listar() {
    const res = await fetch("http://localhost:3001/usuarios")
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
        table.remove()
    }
    
}

listar()