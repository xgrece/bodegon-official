from sqlalchemy.orm import Session
from .models import Cliente, Mesa
from .schemas import ClienteCreate, ClienteUpdate, MesaCreate, MesaUpdate, PedidoCreate, Pedido, PedidoUpdate
from app import models, schemas
from sqlalchemy.exc import IntegrityError

#==================================== C L I E N T E S ========================================

def create_cliente(db: Session, cliente: schemas.ClienteCreate):
    db_cliente = models.Cliente(nombre=cliente.nombre, apellido=cliente.apellido, email=cliente.email,telefono=cliente.telefono)
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def get_cliente(db: Session, cliente_id: int):
    return db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()

def get_clientes(db: Session):
    return db.query(models.Cliente).all()

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

def get_mesa(db: Session, mesa_id: int):
    return db.query(Mesa).filter(Mesa.id == mesa_id).first()

def get_all_mesas(db: Session):
    return db.query(Mesa).all()

def update_mesa(db: Session, mesa_id: int, mesa_data: MesaUpdate):
    db_mesa = db.query(models.Mesa).filter(models.Mesa.id == mesa_id).first()
    if db_mesa:
        db_mesa.capacidad = mesa_data.capacidad  # Actualiza solo la capacidad
        db_mesa.disponible = mesa_data.disponible  # Actualiza solo la disponibilidad
        db.commit()
        db.refresh(db_mesa)
        return db_mesa
    return None

def delete_mesa(db: Session, mesa_id: int):
    db_mesa = db.query(Mesa).filter(Mesa.id == mesa_id).first()
    if db_mesa:
        db.delete(db_mesa)
        db.commit()
        
#================================== P E D I D O S ========================================       
        
def create_pedido(db: Session, pedido_data: PedidoCreate):
    db_pedido = Pedido(**pedido_data.dict())
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

def get_pedido(db: Session, pedido_id: int):
    return db.query(Pedido).filter(Pedido.id == pedido_id).first()

def get_all_pedidos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Pedido).offset(skip).limit(limit).all()

def update_pedido(db: Session, pedido_id: int, pedido_data: PedidoUpdate):
    db_pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if db_pedido:
        for key, value in pedido_data.dict().items():
            setattr(db_pedido, key, value)
        db.commit()
        db.refresh(db_pedido)
        return db_pedido
    return None

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

def get_combo(db: Session, combo_id: int):
    return db.query(models.Combo).filter(models.Combo.id == combo_id).first()

def get_combos(db: Session):
    return db.query(models.Combo).all()

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
    # Crear una nueva reserva con todos los campos requeridos
    db_reserva = models.Reserva(
        id_cliente=reserva.id_cliente,  # Asegúrate de usar cliente_id
        mesa_id=reserva.mesa_id,        # Asegúrate de usar mesa_id
        fecha_reserva=reserva.fecha_reserva,  # Añadir la fecha de la reserva
        hora_reserva=reserva.hora_reserva     # Añadir la hora de la reserva
    )
    db.add(db_reserva)  # Añadir la reserva a la sesión
    db.commit()         # Confirmar los cambios en la base de datos
    db.refresh(db_reserva)  # Obtener la instancia actualizada
    return db_reserva

# Obtener todas las reservas
def get_reservas(db: Session):
    return db.query(models.Reserva).all()

# Obtener una reserva por ID
def get_reserva(db: Session, reserva_id: int):
    db_reserva = db.query(models.Reserva).filter(models.Reserva.id == reserva_id).first()
    if db_reserva is None:
        return None
    # Asegurarse de que id_cliente esté presente en db_reserva
    print(db_reserva.id_cliente)  # Verificar si id_cliente tiene un valor
    return db_reserva

# Actualizar una reserva
def update_reserva(db: Session, reserva_id: int, reserva: schemas.ReservaCreate):
    db_reserva = get_reserva(db, reserva_id)
    if db_reserva:
        db_reserva.id_cliente = reserva.id_cliente  # Cambiar cliente_id por id_cliente
        db_reserva.mesa_id = reserva.mesa_id
        db_reserva.fecha_reserva = reserva.fecha_reserva
        db_reserva.hora_reserva = reserva.hora_reserva
        db.commit()
        db.refresh(db_reserva)
        return db_reserva
    return None

# Eliminar una reserva
def delete_reserva(db: Session, reserva_id: int):
    db_reserva = get_reserva(db, reserva_id)
    if db_reserva:
        db.delete(db_reserva)
        db.commit()
        return {"status": "success"}
    return {"status": "error"}
#======================================= CUENTAS ========================================
# Crear una nueva cuenta
def create_cuenta(db: Session, cuenta: schemas.CuentaCreate):
    nueva_cuenta = models.Cuenta(
        total=cuenta.total,
        reserva_id=cuenta.reserva_id,
        metodo_pago=cuenta.metodo_pago
    )
    db.add(nueva_cuenta)
    db.commit()
    db.refresh(nueva_cuenta)
    return nueva_cuenta

# Obtener todas las cuentas
def get_cuentas(db: Session):
    return db.query(models.Cuenta).all()

# Obtener una cuenta por ID
def get_cuenta(db: Session, cuenta_id: int):
    return db.query(models.Cuenta).filter(models.Cuenta.id == cuenta_id).first()

# Actualizar una cuenta
def update_cuenta(db: Session, cuenta_id: int, cuenta: schemas.CuentaCreate):
    db_cuenta = get_cuenta(db, cuenta_id)
    if db_cuenta:
        db_cuenta.id_reserva = cuenta.id_reserva  # Otras propiedades según tu modelo
        db.commit()
        db.refresh(db_cuenta)
        return db_cuenta
    return None

# Eliminar una cuenta
def delete_cuenta(db: Session, cuenta_id: int):
    db_cuenta = get_cuenta(db, cuenta_id)
    if db_cuenta:
        db.delete(db_cuenta)
        db.commit()
        return {"status": "success"}
    return {"status": "error"}