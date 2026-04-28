from flask import Flask, request, jsonify
from flask_cors import CORS
import PrediccionGasolina

idGas= '' 
ano = '' 
mes = '' 
tipo = ''

consultaValida = 0
app = Flask(__name__)
CORS(app)

@app.route('/getUserData', methods=['GET'])

def getUserData():
    idGas = int(request.args.get('id_gas'))
    ano = int(request.args.get('ano'))
    mes = int(request.args.get('mes'))
    tipo = request.args.get('tipo').lower()
    try:
        if tipo == "regular":
            
            p5,p50,p95 =  PrediccionGasolina.simulacionesMonteCarloReg(idGas, ano, mes)
            consultaValida = 1
        elif tipo == "premium":
            p5,p50,p95 =  PrediccionGasolina.simulacionesMonteCarloPrem(idGas, ano, mes)
            consultaValida = 1
        elif tipo == "diesel":
            p5,p50,p95 = PrediccionGasolina.simulacionesMonteCarloDies(idGas, ano, mes)
            consultaValida = 1
        else: 
            return jsonify({"error": "Tipo no válido"}), 400
            consultaValida = 0

        if consultaValida == 1:
            return jsonify({
                "p5": p5,
                "p50": p50,
                "p95": p95
            })
        
    except Exception as e:
         return jsonify({"error": f"Error en el servidor: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)