from sqlalchemy.orm import Session
from .models import Cliente, Mesa, DetalleCuenta
from .schemas import ClienteCreate, ClienteUpdate, MesaCreate, MesaUpdate, PedidoCreate, Pedido, PedidoUpdate
from app import models, schemas
from sqlalchemy.exc import IntegrityError
from datetime import datetime
#==================================== C L I E N T E S ========================================

def create_cliente(db: Session, cliente: schemas.ClienteCreate):
    db_cliente = models.Cliente(nombre=cliente.nombre, apellido=cliente.apellido, email=cliente.email,telefono=cliente.telefono)
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def get_cliente(db: Session, cliente_id: int):
    return db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def get_clientes(db: Session):
    return db.query(models.Cliente).all()

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def update_cliente(db: Session, cliente_id: int, cliente_data: schemas.ClienteUpdate):
    db_cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if db_cliente:
        db_cliente.nombre = cliente_data.nombre
        db_cliente.apellido = cliente_data.apellido
        db_cliente.email = cliente_data.email
        db_cliente.telefono = cliente_data.telefono  # Actualizar el campo de teléfono
        db.commit()
        db.refresh(db_cliente)
        return db_cliente
    return None

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def delete_cliente(db: Session, cliente_id: int):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        return {"status": "error", "message": "Cliente no encontrado"}
    
    db.delete(cliente)
    db.commit()
    
    return {"status": "success", "message": "Cliente eliminado correctamente"}

#===================================== M E S A S ========================================

def create_mesa(db: Session, mesa_data: schemas.MesaCreate):
    nueva_mesa = models.Mesa(**mesa_data.dict())
    db.add(nueva_mesa)
    db.commit()
    db.refresh(nueva_mesa)
    return nueva_mesa

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def get_mesa(db: Session, mesa_id: int):
    return db.query(Mesa).filter(Mesa.id == mesa_id).first()

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def get_all_mesas(db: Session):
    return db.query(models.Mesa).all()

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def update_mesa(db: Session, mesa_id: int, mesa_data: schemas.MesaUpdate):
    mesa = db.query(models.Mesa).filter(models.Mesa.id == mesa_id).first()
    if mesa:
        mesa.capacidad = mesa_data.capacidad
        mesa.disponible = mesa_data.disponible
        db.commit()  # Guarda los cambios en la base de datos
        db.refresh(mesa)  # Opcional, para refrescar el objeto desde la base de datos
        return mesa
    return None

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def delete_mesa(db: Session, mesa_id: int):
    db_mesa = db.query(Mesa).filter(Mesa.id == mesa_id).first()
    if db_mesa:
        db.delete(db_mesa)
        db.commit()
        
#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//
        
def get_mesas_disponibles(db: Session):
    return db.query(models.Mesa).filter(models.Mesa.disponible == True).all()
        
#================================== P E D I D O S ========================================       
        
def create_pedido(db: Session, pedido: PedidoCreate):
    db_pedido = models.Pedido(**pedido.dict())
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def get_pedidos(db: Session):
    return db.query(models.Pedido).all()

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def get_pedido(db: Session, pedido_id: int):
    return db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def update_pedido_estado(db: Session, pedido_id: int, estado: str):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if pedido:
        pedido.estado = estado
        db.commit()
        db.refresh(pedido)
    return pedido

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def delete_pedido(db: Session, pedido_id: int):
    db_pedido = db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()
    if db_pedido:
        db.delete(db_pedido)
        db.commit()
    return db_pedido


#======================================= COMBOS ========================================

def create_combo(db: Session, combo_data: schemas.ComboCreate, ingredientes: list[str]):
    # Crear combo
    db_combo = models.Combo(
        nombre=combo_data.nombre,
        descripcion=combo_data.descripcion,
        precio=combo_data.precio
    )
    
    db.add(db_combo)
    db.commit()
    db.refresh(db_combo)

    # Asociar los ingredientes al combo
    for ingrediente in ingredientes:
        db_ingrediente = models.Ingrediente(nombre=ingrediente, combo_id=db_combo.id)
        db.add(db_ingrediente)

    db.commit()
    
    return db_combo

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def get_combo(db: Session, combo_id: int):
    return db.query(models.Combo).filter(models.Combo.id == combo_id).first()

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def get_combos(db: Session):
    return db.query(models.Combo).all()

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def update_combo(db: Session, combo_id: int, combo_data: schemas.ComboUpdate):
    db_combo = db.query(models.Combo).filter(models.Combo.id == combo_id).first()
    if db_combo:
        db_combo.nombre = combo_data.nombre
        db_combo.descripcion = combo_data.descripcion
        db_combo.precio = combo_data.precio
        db.commit()
        db.refresh(db_combo)
        return db_combo
    return None

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def delete_combo(db: Session, combo_id: int):
    combo = db.query(models.Combo).filter(models.Combo.id == combo_id).first()
    if combo:
        db.delete(combo)
        db.commit()
        return {"status": "success", "message": "Combo eliminado correctamente"}
    return {"status": "error", "message": "Combo no encontrado"}

#======================================= INGREDIENTES ========================================
def get_ingredientes_por_combo(db: Session, combo_id: int):
    return db.query(models.Ingrediente).filter(models.Ingrediente.combo_id == combo_id).all()

#======================================= RESERVAS ========================================
# Crear una nueva reserva
def create_reserva(db: Session, reserva: schemas.ReservaCreate):
    db_reserva = models.Reserva(
        cliente_id=reserva.cliente_id,
        mesa_id=reserva.mesa_id,
        fecha_reserva=reserva.fecha_reserva,
        hora_reserva=reserva.hora_reserva
    )
    db.add(db_reserva)
    db.commit()
    db.refresh(db_reserva)
    return db_reserva

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

# Obtener todas las reservas
def get_reservas(db: Session):
    return db.query(models.Reserva).all()

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

# Obtener una reserva por ID
def get_reserva(db: Session, reserva_id: int):
    db_reserva = db.query(models.Reserva).filter(models.Reserva.id == reserva_id).first()
    if db_reserva is None:
        return None
    # Asegurarse de que  cliente_id esté presente en db_reserva
    print(db_reserva. cliente_id)  # Verificar si  cliente_id tiene un valor
    return db_reserva

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

# Actualizar una reserva
def update_reserva(db: Session, reserva_id: int, reserva_data: schemas.ReservaUpdate):
    db_reserva = db.query(models.Reserva).filter(models.Reserva.id == reserva_id).first()
    if db_reserva:
        # Solo actualizar fecha y hora
        db_reserva.fecha = reserva_data.fecha
        db_reserva.hora = reserva_data.hora
        db.commit()
        db.refresh(db_reserva)
        return db_reserva
    return None

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

# Eliminar una reserva
def delete_reserva(db: Session, reserva_id: int):
    db_reserva = get_reserva(db, reserva_id)
    if db_reserva:
        db.delete(db_reserva)
        db.commit()
        return {"status": "success"}
    return {"status": "error"}


#======================================= CUENTAS ========================================

# Obtener todas las cuentas
def get_cuentas(db: Session):
    return db.query(models.Cuenta).all()

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

# Obtener una cuenta por ID
def get_cuenta(db: Session, cuenta_id: int):
    return db.query(models.Cuenta).filter(models.Cuenta.id == cuenta_id).first()

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

# Actualizar una cuenta
def update_cuenta(db: Session, cuenta_id: int, cuenta: schemas.CuentaCreate):
    db_cuenta = get_cuenta(db, cuenta_id)
    if db_cuenta:
        db_cuenta.mesa_id = cuenta.mesa_id  # Actualiza otros campos según tu modelo
        db.commit()
        db.refresh(db_cuenta)
        return db_cuenta
    return None

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

# Eliminar una cuenta
def delete_cuenta(db: Session, cuenta_id: int):
    db_cuenta = get_cuenta(db, cuenta_id)
    if db_cuenta:
        db.delete(db_cuenta)
        db.commit()
        return {"status": "success"}
    return {"status": "error"}

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

# Abrir una cuenta
def abrir_cuenta(db: Session, cuenta_data: schemas.CuentaCreate):
    # Verificar si la mesa ya tiene una cuenta abierta
    cuenta_existente = db.query(models.Cuenta).filter(
        models.Cuenta.mesa_id == cuenta_data.mesa_id,
        models.Cuenta.estado == "abierta"
    ).first()
    
    if cuenta_existente:
        # Retorna None o algún valor que puedas usar para indicar que ya existe una cuenta
        return None
    
    # Crear la nueva cuenta
    nueva_cuenta = models.Cuenta(
        mesa_id=cuenta_data.mesa_id,
        fecha_apertura=datetime.now().date(),
        estado="abierta",
        total=0.0
    )
    
    # Marcar la mesa como ocupada
    mesa = db.query(models.Mesa).filter(models.Mesa.id == cuenta_data.mesa_id).first()
    mesa.disponible = False
    
    db.add(nueva_cuenta)
    db.commit()
    db.refresh(nueva_cuenta)
    return nueva_cuenta

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

# Agregar un producto a una cuenta
def agregar_producto_a_cuenta(db: Session, cuenta_id: int, producto_id: int, cantidad: int, tipo_producto: str):
    if tipo_producto == "bebida":
        producto = db.query(models.Bebida).filter(models.Bebida.id == producto_id).first()
    elif tipo_producto == "combo":
        producto = db.query(models.Combo).filter(models.Combo.id == producto_id).first()
    else:
        return None  # Tipo de producto no válido

    if producto is None:
        return None  # Producto no encontrado

    # Calcular subtotal
    precio_unitario = producto.precio
    subtotal = precio_unitario * cantidad

    # Crear el detalle de cuenta
    detalle = DetalleCuenta(
        cuenta_id=cuenta_id,
        producto_id=producto_id,
        cantidad=cantidad,
        precio_unitario=precio_unitario,
        subtotal=subtotal,
    )
    print("Cuenta ID:", cuenta_id)
    print("Productos recibidos:", producto_id)  # Añadir línea de depuración
    print("Cantidad recibida:", cantidad)  # Añadir línea de depuración
    db.add(detalle)
    db.commit()
    db.refresh(detalle)
    return detalle

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

# Cerrar una cuenta
def cerrar_cuenta(db: Session, cuenta_id: int):
    cuenta = db.query(models.Cuenta).filter(models.Cuenta.id == cuenta_id).first()
    if not cuenta:
        return None  # Manejar el error adecuadamente
    
    cuenta.estado = "cerrada"
    cuenta.fecha_cierre = datetime.now()
    
    # Liberar la mesa asociada a la cuenta
    mesa = db.query(models.Mesa).filter(models.Mesa.id == cuenta.mesa_id).first()
    mesa.disponible = True
    
    db.commit()
    return cuenta


#======================================= B E B I D A S ========================================
def create_bebida(db: Session, bebida: schemas.BebidaCreate):
    db_bebida = models.Bebida(**bebida.dict())
    db.add(db_bebida)
    db.commit()
    db.refresh(db_bebida)
    return db_bebida

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def get_bebidas(db: Session):
    return db.query(models.Bebida).all()

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def get_bebida(db: Session, bebida_id: int):
    return db.query(models.Bebida).filter(models.Bebida.id == bebida_id).first()

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//
def update_bebida(db: Session, bebida_id: int, bebida_data: schemas.BebidaUpdate):
    # Buscar la bebida en la base de datos
    db_bebida = db.query(models.Bebida).filter(models.Bebida.id == bebida_id).first()
    
    # Verificar si la bebida existe
    if db_bebida:
        # Actualizar los campos de la bebida
        db_bebida.nombre = bebida_data.nombre
        db_bebida.precio = bebida_data.precio
        # Confirmar los cambios en la base de datos
        db.commit()
        # Refrescar el objeto para obtener los datos actualizados
        db.refresh(db_bebida)
        return db_bebida  # Devolver el objeto actualizado
    return None 
#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//
def delete_bebida(db: Session, bebida_id: int):
    bebida = db.query(models.Bebida).filter(models.Bebida.id == bebida_id).first()
    if bebida:
        db.delete(bebida)
        db.commit()
        return {"status": "success", "message": "Bebida eliminada con éxito"}
    return {"status": "error", "message": "Bebida no encontrada"}

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//
#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//
def get_combo_by_id(db: Session, combo_id: int):
    return db.query(models.Combo).filter(models.Combo.id == combo_id).first()

def get_pedido_by_id(db: Session, pedido_id: int):
    return db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()

def get_bebida_by_id(db: Session, bebida_id: int):
    return db.query(models.Bebida).filter(models.Bebida.id == bebida_id).first()


def get_combo_precio(db: Session, combo_id: int) -> float:
    combo = get_combo_by_id(db, combo_id)
    if combo:
        return combo.precio  # Asegúrate de que el objeto combo tenga un atributo 'precio'
    return 0.0


def get_bebida_precio(db: Session, bebida_id: int) -> float:
    bebida = get_bebida_by_id(db, bebida_id)
    if bebida:
        return bebida.precio  # Asegúrate de que el objeto bebida tenga un atributo 'precio'
    return 0.0

def get_pedidos_finalizados(db: Session):
    return db.query(models.Pedido).filter(models.Pedido.estado == 'finalizado').all()

