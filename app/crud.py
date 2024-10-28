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
        
def create_pedido(db: Session, pedido_data: PedidoCreate):
    db_pedido = Pedido(**pedido_data.dict())
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def get_pedido(db: Session, pedido_id: int):
    return db.query(Pedido).filter(Pedido.id == pedido_id).first()

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def get_all_pedidos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Pedido).offset(skip).limit(limit).all()

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def update_pedido(db: Session, pedido_id: int, pedido_data: PedidoUpdate):
    db_pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if db_pedido:
        for key, value in pedido_data.dict().items():
            setattr(db_pedido, key, value)
        db.commit()
        db.refresh(db_pedido)
        return db_pedido
    return None

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def delete_pedido(db: Session, pedido_id: int):
    db_pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if db_pedido:
        db.delete(db_pedido)
        db.commit()
        return {"message": "Pedido eliminado"}
    return {"message": "Pedido no encontrado"}



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
def update_reserva(db: Session, reserva_id: int, reserva: schemas.ReservaCreate):
    db_reserva = get_reserva(db, reserva_id)
    if db_reserva:
        db_reserva.cliente_id = reserva.cliente_id
        db_reserva.mesa_id = reserva.mesa_id
        db_reserva.fecha_reserva = reserva.fecha_reserva
        db_reserva.hora_reserva = reserva.hora_reserva  # No es necesario el .time()
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
def agregar_producto_a_cuenta(db: Session, cuenta_id: int, producto_id: int, cantidad: int):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        return None

    # Calcular el subtotal y el precio unitario
    precio_unitario = producto.precio
    subtotal = precio_unitario * cantidad

    # Crear un nuevo detalle de cuenta
    nuevo_detalle = DetalleCuenta(
        cuenta_id=cuenta_id,
        producto_id=producto_id,
        cantidad=cantidad,
        precio_unitario=precio_unitario,
        subtotal=subtotal
    )
    
    db.add(nuevo_detalle)
    db.commit()  # Asegúrate de hacer commit aquí para guardar los cambios
    db.refresh(nuevo_detalle)
    return nuevo_detalle

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

def delete_bebida(db: Session, bebida_id: int):
    bebida = db.query(models.Bebida).filter(models.Bebida.id == bebida_id).first()
    if bebida:
        db.delete(bebida)
        db.commit()
        return {"status": "success", "message": "Bebida eliminada con éxito"}
    return {"status": "error", "message": "Bebida no encontrada"}

