from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'

# Datos de proyectos y habilidades
PROYECTOS = [
    {
        'titulo': 'Sistema de Gestión de Tareas',
        'descripcion': 'Aplicación web para gestionar tareas personales con Flask',
        'tecnologias': ['Python', 'Flask', 'SQLite', 'HTML/CSS'],
        'url': '#'
    },
    {
        'titulo': 'Portfolio Personal',
        'descripcion': 'Portafolio dinámico para mostrar proyectos y habilidades',
        'tecnologias': ['Flask', 'Jinja2', 'Bootstrap', 'Python'],
        'url': '#'
    },
    {
        'titulo': 'API REST',
        'descripcion': 'API REST para gestión de usuarios y datos',
        'tecnologias': ['Python', 'Flask', 'JSON', 'RESTful'],
        'url': '#'
    }
]

HABILIDADES = [
    {'nombre': 'Python', 'nivel': 90},
    {'nombre': 'Flask', 'nivel': 85},
    {'nombre': 'HTML/CSS', 'nivel': 80},
    {'nombre': 'JavaScript', 'nivel': 75},
    {'nombre': 'SQL', 'nivel': 80},
    {'nombre': 'Git', 'nivel': 85}
]

MENSAJES_FILE = 'mensajes_contacto.json'

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/portafolio')
def portafolio():
    return render_template('portafolio.html', proyectos=PROYECTOS, habilidades=HABILIDADES)

@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        asunto = request.form.get('asunto')
        mensaje = request.form.get('mensaje')
        
        # Validar datos
        if not all([nombre, email, asunto, mensaje]):
            flash('Por favor completa todos los campos', 'error')
            return redirect(url_for('contacto'))
        
        # Guardar mensaje
        nuevo_mensaje = {
            'nombre': nombre,
            'email': email,
            'asunto': asunto,
            'mensaje': mensaje,
            'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        try:
            # Leer mensajes existentes
            if os.path.exists(MENSAJES_FILE):
                with open(MENSAJES_FILE, 'r') as f:
                    mensajes = json.load(f)
            else:
                mensajes = []
            
            # Agregar nuevo mensaje
            mensajes.append(nuevo_mensaje)
            
            # Guardar mensajes
            with open(MENSAJES_FILE, 'w') as f:
                json.dump(mensajes, f, indent=4)
            
            flash('¡Mensaje enviado correctamente! Te contactaremos pronto.', 'exito')
        except Exception as e:
            flash(f'Error al enviar el mensaje: {str(e)}', 'error')
        
        return redirect(url_for('contacto'))
    
    return render_template('contacto.html')

if __name__ == '__main__':
    app.run(debug=True)
