
import sqlite3

conn = sqlite3.connect("inventario.db")
cursor = conn.cursor()

def actualizar_stock():
    id = input("Ingrese el ID del producto para actualizar stock: ").strip()
    if not id.isdigit():
        print("ID inválido.")
        return
    cursor.execute("SELECT * FROM productos WHERE id = ?", (int(id),))
    producto = cursor.fetchone()
    if not producto:
        print("Producto no encontrado.")
        return
    print(f"Stock actual de {producto[1]}: {producto[4]}")
    nuevo_stock = input("Ingrese el nuevo stock: ").strip()
    if not nuevo_stock.isdigit():
        print("Stock inválido.")
        return
    cursor.execute("UPDATE productos SET stock = ? WHERE id = ?", (int(nuevo_stock), int(id)))
    conn.commit()
    print("Stock actualizado correctamente.")

def actualizar_precio():
    id = input("Ingrese el ID del producto para actualizar precio: ").strip()
    if not id.isdigit():
        print("ID inválido.")
        return
    cursor.execute("SELECT * FROM productos WHERE id = ?", (int(id),))
    producto = cursor.fetchone()
    if not producto:
        print("Producto no encontrado.")
        return
    print(f"Precio actual de {producto[1]}: ${producto[3]}")
    nuevo_precio = input("Ingrese el nuevo precio: ").strip()
    if not nuevo_precio.isdigit():
        print("Precio inválido.")
        return
    cursor.execute("UPDATE productos SET precio = ? WHERE id = ?", (int(nuevo_precio), int(id)))
    conn.commit()
    print("Precio actualizado correctamente.")

def exportar_productos_a_txt():
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    if not productos:
        print("No hay productos para exportar.")
        return
    with open("productos_exportados.txt", "w", encoding="utf-8") as archivo:
        for prod in productos:
            linea = f"{prod[0]}. Nombre: {prod[1]}, Categoría: {prod[2]}, Precio: ${prod[3]}, Stock: {prod[4]}\n"
            archivo.write(linea)
    print("Productos exportados a productos_exportados.txt exitosamente.")
