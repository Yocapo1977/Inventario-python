
import sqlite3
from colorama import init, Fore, Style

init(autoreset=True)

conn = sqlite3.connect("inventario.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    categoria TEXT NOT NULL,
    precio INTEGER NOT NULL,
    stock INTEGER NOT NULL
)
""")
conn.commit()

def imprimir_titulo(texto):
    print(Fore.CYAN + Style.BRIGHT + "\n" + texto.center(50, "=") + "\n")

def imprimir_error(texto):
    print(Fore.RED + "Error: " + texto)

def imprimir_exito(texto):
    print(Fore.GREEN + "✔ " + texto)

def agregar_producto():
    while True:
        nombre = input("Nombre del producto: ").strip().capitalize()
        if not nombre:
            imprimir_error("Debe ingresar un nombre.")
            continue
        categoria = input("Categoría: ").strip().capitalize()
        if not categoria:
            imprimir_error("Debe ingresar una categoría.")
            continue
        precio = input("Precio: ")
        if not precio.isdigit() or int(precio) <= 0:
            imprimir_error("El precio debe ser un número mayor a 0.")
            continue
        stock = input("Stock: ")
        if not stock.isdigit() or int(stock) < 0:
            imprimir_error("El stock debe ser un número válido.")
            continue
        cursor.execute("INSERT INTO productos (nombre, categoria, precio, stock) VALUES (?, ?, ?, ?)",
                       (nombre, categoria, int(precio), int(stock)))
        conn.commit()
        imprimir_exito(f"Producto '{nombre}' agregado.")
        seguir = input("¿Agregar otro producto? (s/n): ").strip().lower()
        if seguir != "s":
            break

def mostrar_productos():
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    if not productos:
        imprimir_error("No hay productos.")
    else:
        imprimir_titulo("Lista de Productos")
        for prod in productos:
            print(f"{prod[0]}. {Fore.YELLOW}{prod[1]}{Style.RESET_ALL} | Categoría: {prod[2]} | Precio: ${prod[3]} | Stock: {prod[4]}")

def buscar_producto():
    while True:
        tipo = input("Buscar por 'nombre' o 'id': ").strip().lower()
        if tipo == "nombre":
            nombre = input("Nombre del producto: ").strip().capitalize()
            cursor.execute("SELECT * FROM productos WHERE nombre = ?", (nombre,))
        elif tipo == "id":
            id = input("ID del producto: ").strip()
            if not id.isdigit():
                imprimir_error("ID inválido.")
                continue
            cursor.execute("SELECT * FROM productos WHERE id = ?", (int(id),))
        else:
            imprimir_error("Opción no válida.")
            continue
        resultado = cursor.fetchall()
        if resultado:
            for prod in resultado:
                print(f"{prod[0]}. {prod[1]} - Categoría: {prod[2]}, Precio: ${prod[3]}, Stock: {prod[4]}")
        else:
            imprimir_error("Producto no encontrado.")
        seguir = input("¿Buscar otro producto? (s/n): ").strip().lower()
        if seguir != "s":
            break

def modificar_producto():
    mostrar_productos()
    id = input("ID del producto a modificar: ").strip()
    if not id.isdigit():
        imprimir_error("ID inválido.")
        return
    cursor.execute("SELECT * FROM productos WHERE id = ?", (int(id),))
    producto = cursor.fetchone()
    if not producto:
        imprimir_error("Producto no encontrado.")
        return
    print(f"Actual: {producto}")
    nuevo_nombre = input("Nuevo nombre (enter para dejar igual): ").strip().capitalize()
    nueva_categoria = input("Nueva categoría (enter para dejar igual): ").strip().capitalize()
    nuevo_precio = input("Nuevo precio (enter para dejar igual): ").strip()
    nuevo_stock = input("Nuevo stock (enter para dejar igual): ").strip()

    cursor.execute("""
        UPDATE productos SET
            nombre = ?,
            categoria = ?,
            precio = ?,
            stock = ?
        WHERE id = ?
    """, (
        nuevo_nombre if nuevo_nombre else producto[1],
        nueva_categoria if nueva_categoria else producto[2],
        int(nuevo_precio) if nuevo_precio.isdigit() else producto[3],
        int(nuevo_stock) if nuevo_stock.isdigit() else producto[4],
        int(id)
    ))
    conn.commit()
    imprimir_exito("Producto modificado correctamente.")

def eliminar_producto():
    mostrar_productos()
    id = input("ID del producto a eliminar: ").strip()
    if not id.isdigit():
        imprimir_error("ID inválido.")
        return
    cursor.execute("SELECT * FROM productos WHERE id = ?", (int(id),))
    producto = cursor.fetchone()
    if not producto:
        imprimir_error("Producto no encontrado.")
        return
    print(f"Eliminar: {producto[1]}, Precio: ${producto[3]}, Stock: {producto[4]}")
    confirmar = input("¿Confirmás eliminar este producto? (s/n): ").strip().lower()
    if confirmar == "s":
        cursor.execute("DELETE FROM productos WHERE id = ?", (int(id),))
        conn.commit()
        imprimir_exito("Producto eliminado.")
    else:
        print("Eliminación cancelada.")

def reporte_bajo_stock():
    limite = input("Stock mínimo para alerta: ").strip()
    if not limite.isdigit():
        imprimir_error("Debe ingresar un número válido.")
        return
    cursor.execute("SELECT * FROM productos WHERE stock < ?", (int(limite),))
    productos = cursor.fetchall()
    if productos:
        imprimir_titulo("Productos con Bajo Stock")
        for prod in productos:
            print(f"{prod[1]} - Stock: {Fore.RED}{prod[4]}{Style.RESET_ALL}")
    else:
        imprimir_exito("Todos los productos tienen stock suficiente.")

def actualizar_stock():
    id = input("ID del producto: ").strip()
    if not id.isdigit():
        imprimir_error("ID inválido.")
        return
    cursor.execute("SELECT * FROM productos WHERE id = ?", (int(id),))
    producto = cursor.fetchone()
    if not producto:
        imprimir_error("Producto no encontrado.")
        return
    print(f"Stock actual de {producto[1]}: {producto[4]}")
    nuevo_stock = input("Nuevo stock: ").strip()
    if not nuevo_stock.isdigit():
        imprimir_error("Stock inválido.")
        return
    cursor.execute("UPDATE productos SET stock = ? WHERE id = ?", (int(nuevo_stock), int(id)))
    conn.commit()
    imprimir_exito("Stock actualizado.")

def actualizar_precio():
    id = input("ID del producto: ").strip()
    if not id.isdigit():
        imprimir_error("ID inválido.")
        return
    cursor.execute("SELECT * FROM productos WHERE id = ?", (int(id),))
    producto = cursor.fetchone()
    if not producto:
        imprimir_error("Producto no encontrado.")
        return
    print(f"Precio actual de {producto[1]}: ${producto[3]}")
    nuevo_precio = input("Nuevo precio: ").strip()
    if not nuevo_precio.isdigit():
        imprimir_error("Precio inválido.")
        return
    cursor.execute("UPDATE productos SET precio = ? WHERE id = ?", (int(nuevo_precio), int(id)))
    conn.commit()
    imprimir_exito("Precio actualizado.")

def exportar_productos_a_txt():
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    if not productos:
        imprimir_error("No hay productos para exportar.")
        return
    with open("productos_exportados.txt", "w", encoding="utf-8") as archivo:
        for prod in productos:
            archivo.write(f"{prod[0]}. Nombre: {prod[1]}, Categoría: {prod[2]}, Precio: ${prod[3]}, Stock: {prod[4]}\n")
    imprimir_exito("Productos exportados a productos_exportados.txt")

def menu():
    while True:
        imprimir_titulo("MENÚ DE INVENTARIO")
        print("1. Agregar producto")
        print("2. Mostrar productos")
        print("3. Buscar producto")
        print("4. Modificar producto")
        print("5. Eliminar producto")
        print("6. Reporte bajo stock")
        print("7. Actualizar stock")
        print("8. Actualizar precio")
        print("9. Exportar productos a TXT")
        print("10. Salir")

        opcion = input("Opción: ").strip()
        if opcion == "1":
            agregar_producto()
        elif opcion == "2":
            mostrar_productos()
        elif opcion == "3":
            buscar_producto()
        elif opcion == "4":
            modificar_producto()
        elif opcion == "5":
            eliminar_producto()
        elif opcion == "6":
            reporte_bajo_stock()
        elif opcion == "7":
            actualizar_stock()
        elif opcion == "8":
            actualizar_precio()
        elif opcion == "9":
            exportar_productos_a_txt()
        elif opcion == "10":
            print("Gracias por usar el sistema.")
            break
        else:
            imprimir_error("Opción inválida.")

menu()
conn.close()
