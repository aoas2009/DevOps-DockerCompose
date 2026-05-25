from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

def get_conn():
    return psycopg2.connect(os.environ["DATABASE_URL"])

@app.route("/usuarios")
def usuarios():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuarios")
    rows = cur.fetchall()
    conn.close()
    return jsonify(rows)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3001)
    
#para conectar externamente no banco:
# Criar banco
# docker run --name bancoexterno -e POSTGRES_PASSWORD=senha123 -p 5432:5432 -v devops_dockcomp_dados_postgres:/var/lib/postgresql/data -d postgres

# Conectar
# docker exec -it bancoexterno psql -U admin -d banco