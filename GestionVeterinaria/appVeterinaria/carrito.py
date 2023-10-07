class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get("carrito")
        if not carrito:
            self.session["carrito"] = {}
            self.carrito = self.session["carrito"]
        else:
            self.carrito = carrito
    

    def agregar(self, producto):
        id = str(producto.id)
        descuento = 0
        if producto.proEstado == "Promocion":
            descuento = producto.proDescuento
            precio = producto.proPrecio
            deci = descuento / 100
            descuentoPorUnidad = precio * deci
        else: 
            descuentoPorUnidad = 0
        if id not in self.carrito.keys():
            self.carrito[id]={
                "producto_id": producto.id,
                "nombre": producto.proNombre,
                "precioUnidad": producto.proPrecio,
                "porcentajeDescuento": int(descuento),
                "descuento": int(descuentoPorUnidad),
                "acumulado": int(producto.proPrecio - descuentoPorUnidad),
                "imagen": str(producto.proFoto),
                "cantidad": 1
            }
        else:
            self.carrito[id]["cantidad"] += 1
            self.carrito[id]["acumulado"] += producto.proPrecio - descuentoPorUnidad
            
        self.guardar_carrito()

    def guardar_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True

    def eliminar(self, producto):
        id = str(producto.id)
        if id in self.carrito:
            del self.carrito[id]
            self.guardar_carrito()

    def restar(self, producto):
        id = str(producto.id)
        if id in self.carrito.keys():
            self.carrito[id]["cantidad"] -= 1
            self.carrito[id]["acumulado"] -= producto.proPrecio
            if self.carrito[id]["cantidad"] <= 0: self.eliminar(producto)
            self.guardar_carrito()

    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True
        
    def total_carrito(request):
        total = 0
        descuentos = 0 
        if "carrito" in request.session.keys():
                for key, value in request.session["carrito"].items():
                    cantidad = value["cantidad"]
                    descuentoUnidad = value["descuento"]
                    totalDescuentos = cantidad * descuentoUnidad
                    total += int(value["acumulado"])
                    descuentos += totalDescuentos        
        return total, descuentos