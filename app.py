from flask import Flask, render_template, request, redirect, url_for, session, flash
import uuid

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Inicializamos la sesión para guardar productos
def init_session():
    if 'products' not in session:
        session['products'] = []

# Ruta para la página principal
@app.route('/')
def index():
    init_session()
    return render_template('index.html', products=session['products'])

# Ruta para agregar un nuevo producto
@app.route('/add', methods=['POST'])
def add_product():
    init_session()
    # Recoger los datos del formulario
    product = {
        'id': str(uuid.uuid4()),
        'nombre': request.form['nombre'],
        'cantidad': int(request.form['cantidad']),
        'precio': float(request.form['precio']),
        'fecha_vencimiento': request.form['fecha_vencimiento'],
        'categoria': request.form['categoria']
    }
    session['products'].append(product)
    flash('Producto agregado exitosamente', 'success')
    return redirect(url_for('index'))

# Ruta para eliminar un producto
@app.route('/delete/<product_id>', methods=['POST'])
def delete_product(product_id):
    init_session()
    session['products'] = [p for p in session['products'] if p['id'] != product_id]
    flash('Producto eliminado', 'danger')
    return redirect(url_for('index'))

# Ruta para editar un producto
@app.route('/edit/<product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    init_session()
    product = next((p for p in session['products'] if p['id'] == product_id), None)

    if request.method == 'POST':
        # Actualizar el producto
        product['nombre'] = request.form['nombre']
        product['cantidad'] = int(request.form['cantidad'])
        product['precio'] = float(request.form['precio'])
        product['fecha_vencimiento'] = request.form['fecha_vencimiento']
        product['categoria'] = request.form['categoria']
        flash('Producto actualizado correctamente!', 'success')
        return redirect(url_for('index'))

    return render_template('edit.html', product=product)

if __name__ == '__main__':
    app.run(debug=True)
