from flask import Flask, render_template, request, flash
from conexion import obtener_conexion  # Importamos la función desde conexion.py

# Configuración de Flask
app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/security-question/<int:security_question_id>', methods=['GET', 'POST'])
def security_question(security_question_id):
    question_text = ""
    if request.method == 'GET':
        try:
            conn = obtener_conexion()
            with conn.cursor() as cursor:
                query = "SELECT question_text FROM security_questions WHERE question_id = %s"
                cursor.execute(query, (security_question_id,))
                result = cursor.fetchone()
                if result:
                    question_text = result[0]
                else:
                    flash("Pregunta de seguridad no encontrada.", "error")
        except Exception as e:
            flash(f"Error al conectar con la base de datos: {e}", "error")
        finally:
            conn.close()

    if request.method == 'POST':
        user_response = request.form.get('answer')
        try:
            conn = obtener_conexion()
            with conn.cursor() as cursor:
                query = """
                    SELECT answer 
                    FROM security_questions 
                    WHERE question_id = %s
                """
                cursor.execute(query, (security_question_id,))
                result = cursor.fetchone()
                if result and user_response == result[0]:
                    flash("Respuesta correcta.", "success")
                else:
                    flash("Respuesta incorrecta.", "error")
        except Exception as e:
            flash(f"Error al conectar con la base de datos: {e}", "error")
        finally:
            conn.close()

    return render_template('Preguntas.html', question_text=question_text)

if __name__ == '__main__':
    app.run(debug=True)
