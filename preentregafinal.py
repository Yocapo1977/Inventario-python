print("\n===== Gestión de Inventario ====")

productos = []

while True:
    print("\n********************")
    print("Menú:")
    print("********************")
    print("1.- Agregar producto:")
    print("2.- Mostrar productos:")
    print("3.- Buscar producto:")
    print("4.- Eliminar producto:")
    print("5.- Salir.")

    opcion = input(f"\nIngresa el número de la opción deseada: ")

    if opcion == "1":
        while True:
            nombre = input("Ingrese el nombre del producto: ").strip().capitalize()
            if nombre == "":
                print("Debe ingresar un nombre para poder continuar...")
                continue
            categoria = input("Ingrese la categoría del producto: ").strip().capitalize()
            if categoria == "":
                print("Debe al menos escribir una categoría para continuar...")
                continue
            precio = input("Ingrese el precio del producto: ")
            
            if not precio.isdigit() or int(precio) <= 0:
                print("El precio deber ser indicado en un N° mayor a cero.")
                continue
            precio = int(precio)
            productos.append([nombre, categoria, precio])
            print(f"El producto '{nombre}' fue agregado exitosamente")

            seguir = input("Desea agregar otro producto a la lista? (s/n):").strip().lower()
            if seguir != "s":
                break
    elif opcion == "2":
        if not productos:
            print("No hay productos dentro de la lista.")
        else:
            print("\n****** Lista de productos ingresados ******")
            i = 1
            for producto in productos:                
                print(f"{i}.Nombre: {producto[0]}, Categoría: {producto[1]}, Precio: $ {producto[2]}")  
                i += 1

    elif opcion == "3":
        
            print("\n*****************")
            print("Buscar productos")
            print("\*****************")
            while True:
                print("\n¿Desea buscar por nombre o por indice?")
                tipo_busqueda = input(" Escriba ' nombre' o 'índice': ").strip().lower()
                if tipo_busqueda == "nombre":
                    buscar = input("Ingrese el producto que desea buscar '{buscar}'? (s/n):").strip().lower()
                    if confirmar != "s":
                        print("Busqueda cancelada por el usuario.")
                    else:
                        encontrado = False
                        for producto in productos:
                            if producto[0] == buscar:
                                print(f"Producto encontrado: Nombre: {producto[0]}, Categoría: {producto[1]}, Precio $: {producto[2]}")
                                encontrado = True
                                break
                            if not encontrado:
                                print("Producto no encontrado.")
                elif tipo_busqueda == "indice" or tipo_busqueda == "índice":
                    if not productos:
                        print("no hay productos en la lista.")
                        break
                    indice = input("Ingrese el índice del producto (empezando en 1):").strip()
                    if not indice.isdigit() or int(indice) <= 0 or int(indice) > len(productos):
                        print("Índice inválido. Intente nuevamente.")
                    else:
                        idx = int(indice) - 1
                        producto = productos[idx]
                        print(f"Producto en el índice {indice}: Nombre: {producto[0]}, Categoría: {producto[1]}. Precio: $ {producto[2]}")
                else:
                    print("Opción de búsqueda no válida. Intente con 'nombre' o 'índice'.")
                    seguir = input("¿Desea buscar otro producto? (s/n): ").strip().lower()
                    if seguir != "s":
                        break    
    elif opcion == "4":
        print("Eliminar producto")
        if len(productos) <= 0:
            print("\nNo hay productos cargados en el inventario.\n")
            continue
        print("\nLista de productos:")
        i = 1
        for producto in productos:
            print(f"{i}.{productos}")
            i + 1
            producto_a_eliminar = input("Número del producto a eliminar: ").strip()
            if not producto_a_eliminar.isdigit():
                print("Ingrese un número válido.")
                continue
            producto_a_eliminar = int(producto_a_eliminar)

            if producto_a_eliminar < 1 or producto_a_eliminar > len(productos):
                print("Número de producto inexistente. Reintente.")
                continue
            eliminado = productos.pop(producto_a_eliminar - 1)
            print(f"Producto '{eliminado[0]}' eliminado.")

            seguir = input("¿Desea eliminar otro producto? (s/n): ").strip().lower
            if seguir != "s":
                continue

        
    elif opcion == "5":
        confirmar = input("¿Está seguro que desea salir? (s/n): ").strip().lower()
        if confirmar == "s":
            print("\n***************************")
            print("\nGracias y hasta la proxima")
            break
    else: 
        print("Opción no válida. Intente nuevamente.")