from fastapi import FastAPI

app = FastAPI()

productos = [
    "Activador de brillo",
    "Cera para plásticos interiores",
    "Esponja",
    "Shampoo para lavado",
    "Paños de microfibra"
]


@app.get("/productos")
def obtener_productos():
    return {"productos": productos}


@app.post("/productos")
def agregar_producto(nombre: str):
    productos.append(nombre)
    return {"mensaje": "Producto agregado", "producto": nombre}

@app.put("/productos/{id}")
def actualizar_producto(id: int, nombre: str):
    if id < len(productos):
        productos[id] = nombre
        return {"mensaje": "Producto actualizado", "producto": nombre}
    return {"error": "Producto no encontrado"}


@app.delete("/productos/{id}")
def eliminar_producto(id: int):
    if id < len(productos):
        eliminado = productos.pop(id)
        return {"mensaje": "Producto eliminado", "producto": eliminado}
    return {"error": "Producto no encontrado"}
