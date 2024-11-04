from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import crud, schemas
from fastapi.templating import Jinja2Templates
from app.models import Cliente
from ..models import Mesa
import logging

logging.basicConfig(level=logging.DEBUG)

# Crear un router principal
router = APIRouter()

# Crear un objeto Jinja2Templates
templates = Jinja2Templates(directory="app/templates")

# Dependencia para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#=============================== CLIENTES ================================================

@router.get("/crear_cliente", response_class=HTMLResponse, tags=["Clientes"])
async def show_create_cliente_form(request: Request):
    return templates.TemplateResponse("crear_cliente.html", {"request": request})

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

@router.post("/crear_cliente", response_class=HTMLResponse, tags=["Clientes"])
async def create_cliente(
    request: Request,
    nombre: str = Form(...),
    apellido: str = Form(...),
    email: str = Form(...),
    telefono: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        cliente_data = schemas.ClienteCreate(nombre=nombre, apellido=apellido, email=email, telefono=telefono)
        cliente = crud.create_cliente(db, cliente_data)
        message = f"Cliente {nombre} {apellido} creado exitosamente"
    except Exception as e:
        message = f"Error al crear el cliente: {str(e)}"
    
    return templates.TemplateResponse("crear_cliente.html", {
        "request": request, 
        "message": message
    })

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

@router.get("/read_clientes", response_class=HTMLResponse, tags=["Clientes"])
async def read_clientes(request: Request, db: Session = Depends(get_db), message: str = None):
    clientes = crud.get_clientes(db)
    return templates.TemplateResponse("read_clientes.html", {
        "request": request, 
        "clientes": clientes,
        "message": message  # Pasar mensaje si existe
    })

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

# Obtener un cliente por ID (GET)
@router.get("/clientes/{cliente_id}", response_model=schemas.Cliente, tags=["Clientes"])
async def read_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = crud.get_cliente(db, cliente_id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

@router.post("/clientes/{cliente_id}/actualizar", tags=["Clientes"])
async def actualizar_cliente(
    cliente_id: int, 
    nombre: str = Form(...), 
    apellido: str = Form(...), 
    email: str = Form(...), 
    telefono: str = Form(...),  # Asegúrate de incluir el campo 'telefono'
    db: Session = Depends(get_db)  # Obtener la sesión de la base de datos
):
    try:
        # Llamar a la función de actualización desde crud.py
        cliente_actualizado = crud.update_cliente(
            db, 
            cliente_id, 
            schemas.ClienteUpdate(
                nombre=nombre, 
                apellido=apellido, 
                email=email, 
                telefono=telefono
            )
        )
        if cliente_actualizado is None:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return {"mensaje": "Cliente actualizado exitosamente"}
    except Exception as e:
        print(f"Error actualizando cliente: {e}")
        raise HTTPException(status_code=500, detail="Error interno al actualizar el cliente")
    
#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//    
    
# Eliminar un cliente (POST)
@router.post("/clientes/{cliente_id}/eliminar", response_class=HTMLResponse, tags=["Clientes"])
async def delete_cliente(cliente_id: int, db: Session = Depends(get_db)):
    result = crud.delete_cliente(db, cliente_id)

    if result.get("status") == "success":
        return HTMLResponse(content="Cliente eliminado", status_code=200)
    else:
        return HTMLResponse(content="Error al eliminar el cliente", status_code=400)

#======================================= MESAS ========================================
@router.get("/crear_mesa", response_class=HTMLResponse, tags=["Mesas"])
def get_crear_mesa(request: Request, db: Session = Depends(get_db)):
    clientes = crud.get_clientes(db)  # Cambiado a get_clientes
    return templates.TemplateResponse("crear_mesa.html", {"request": request, "clientes": clientes})

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

@router.post("/crear_mesa", response_class=HTMLResponse, tags=["Mesas"])
def create_mesa(
    request: Request,
    numero_mesa: int = Form(...),
    capacidad: int = Form(...),
    disponible: bool = Form(False),
    db: Session = Depends(get_db)
):
    try:
        # Verifica si los datos son válidos antes de intentar crear la mesa
        if numero_mesa <= 0 or capacidad <= 0:
            raise ValueError("Los valores deben ser mayores a cero.")

        mesa_data = schemas.MesaCreate(
            numero_mesa=numero_mesa,
            capacidad=capacidad,
            disponible=disponible,
            
        )
        crud.create_mesa(db, mesa_data)  # No necesitas asignarlo a `mesa` si no lo usas

        # Redirige de vuelta al formulario o muestra la plantilla de crear mesa nuevamente
        return templates.TemplateResponse("crear_mesa.html", {
            "request": request,
            "success_message": "Mesa creada exitosamente.",  # Mensaje de éxito
            "clientes": crud.get_clientes(db)  # Obtener la lista de clientes
        })
    
    except ValueError as e:
        error_message = str(e)
        return templates.TemplateResponse("crear_mesa.html", {
            "request": request,
            "error_message": error_message,
            "clientes": crud.get_clientes(db)  # Vuelve a obtener la lista de clientes en caso de error
        })
        
#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//        
        
@router.get("/read_mesas", response_class=HTMLResponse, tags=["Mesas"])
async def get_all_mesas(request: Request, db: Session = Depends(get_db)):
    mesas = crud.get_all_mesas(db)  # Asegúrate de que esta función devuelva la lista de mesas
    return templates.TemplateResponse("read_mesas.html", {"request": request, "mesas": mesas})

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

@router.get("/mesas/{mesa_id}", response_model=schemas.Mesa, tags=["Mesas"])
async def get_mesa(mesa_id: int, db: Session = Depends(get_db)):
    mesa = crud.get_mesa(db, mesa_id)
    if mesa is None:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    
    # Devuelve las reservas como objetos completos, no solo IDs
    reservas = [
        {
            "id": reserva.id,
            "fecha_reserva": reserva.fecha_reserva,
            "hora_reserva": reserva.hora_reserva,
            "cliente_id": reserva.cliente_id,
            "mesa_id": reserva.mesa_id
        } 
        for reserva in mesa.reservas
    ] if mesa.reservas else []
    
    return {
        "id": mesa.id,
        "numero_mesa": mesa.numero_mesa,
        "capacidad": mesa.capacidad,
        "disponible": mesa.disponible,
        "reservas": reservas,  # Devuelve objetos completos de reserva
        "cuentas": mesa.cuentas  # Asumiendo que deseas devolver también las cuentas
    }

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

@router.post("/mesas/{mesa_id}/actualizar", tags=["Mesas"])
async def update_mesa(
    mesa_id: int,
    capacidad: int = Form(...),  # Campo para capacidad de la mesa
    disponible: bool = Form(...),  # Campo para disponibilidad de la mesa
    db: Session = Depends(get_db)  # Dependencia de la base de datos
):
    try:
        # Llama al método de CRUD y pasa los campos directamente
        mesa_actualizada = crud.update_mesa(
            db, 
            mesa_id, 
            schemas.MesaUpdate(capacidad=capacidad, disponible=disponible)
        )
        
        if mesa_actualizada is None:
            raise HTTPException(status_code=404, detail="Mesa no encontrada")

        return {
            "mensaje": "Mesa actualizada exitosamente",
            "mesa": {
                "id": mesa_actualizada.id,
                "capacidad": mesa_actualizada.capacidad,
                "disponible": mesa_actualizada.disponible
            }
        }
    except Exception as e:
        print(f"Error actualizando mesa: {e}")
        raise HTTPException(status_code=500, detail="Error interno al actualizar la mesa")

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

@router.delete("/mesas/{mesa_id}/eliminar", response_class=HTMLResponse, tags=["Mesas"])
def delete_mesa(request: Request, mesa_id: int, db: Session = Depends(get_db)):
    crud.delete_mesa(db, mesa_id)
    return templates.TemplateResponse("read_mesas.html", {"request": request, "message": "Mesa eliminada"})

#======================================= PEDIDOS ========================================
@router.get("/crear_pedido", response_class=HTMLResponse, tags=["Pedidos"])
async def create_pedido_form(request: Request):
    return templates.TemplateResponse("crear_pedido.html", {"request": request})

@router.post("/pedidos", response_model=schemas.Pedido)
async def create_pedido(
    mesa_id: int = Form(...),
    combo_id: int = Form(...),
    bebida_id: int = Form(...),
    precio_total: float = Form(...),
    db: Session = Depends(get_db)
):
    pedido_data = schemas.PedidoCreate(
        mesa_id=mesa_id,
        combo_id=combo_id,
        bebida_id=bebida_id,
        precio_total=precio_total
    )
    return crud.create_pedido(db, pedido_data)

@router.get("/pedidos", response_model=list[schemas.Pedido])
async def read_pedidos(db: Session = Depends(get_db)):
    return crud.get_pedidos(db)

@router.get("/pedidos/{pedido_id}", response_model=schemas.Pedido)
async def read_pedido(pedido_id: int, db: Session = Depends(get_db)):
    db_pedido = crud.get_pedido(db, pedido_id)
    if db_pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return db_pedido

@router.put("/pedidos/{pedido_id}", response_model=schemas.Pedido)
async def update_pedido(pedido_id: int, pedido: schemas.PedidoUpdate, db: Session = Depends(get_db)):
    db_pedido = crud.update_pedido(db, pedido_id, pedido)
    if db_pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return db_pedido

@router.delete("/pedidos/{pedido_id}", response_model=schemas.Pedido)
async def delete_pedido(pedido_id: int, db: Session = Depends(get_db)):
    db_pedido = crud.delete_pedido(db, pedido_id)
    if db_pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return db_pedido

#======================================= COMBOS ========================================
# Mostrar el formulario para crear combo (GET)
@router.get("/crear_combo", response_class=HTMLResponse, tags=["Combos"])
async def show_create_combo_form(request: Request):
    return templates.TemplateResponse("crear_combo.html", {"request": request})

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

# Crear un combo (POST)
@router.post("/crear_combo", response_class=HTMLResponse, tags=["Combos"])
async def create_combo(
    request: Request,
    nombre: str = Form(...),
    descripcion: str = Form(...),
    precio: float = Form(...),
    ingredientes: list[str] = Form(...),  # Recibe múltiples ingredientes seleccionados
    db: Session = Depends(get_db)
):
    try:
        # Crear el combo con los ingredientes seleccionados
        combo_data = schemas.ComboCreate(
            nombre=nombre, 
            descripcion=descripcion, 
            precio=precio
        )

        # Llamar a la función para guardar en la base de datos
        combo = crud.create_combo(db, combo_data, ingredientes)
        
        # Mensaje de éxito
        return templates.TemplateResponse("crear_combo.html", {
            "request": request,
            "success_message": f"Combo {nombre} creado exitosamente"
        })

    except Exception as e:
        # Mensaje de error si algo sale mal
        return templates.TemplateResponse("crear_combo.html", {
            "request": request,
            "error_message": f"Error al crear el combo: {str(e)}"
        })

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

# Obtener un combo por ID (GET)
@router.get("/combos/{combo_id}", response_model=schemas.Combo, tags=["Combos"])
async def read_combo(combo_id: int, db: Session = Depends(get_db)):
    combo = crud.get_combo(db, combo_id)
    if combo is None:
        raise HTTPException(status_code=404, detail="Combo no encontrado")
    return combo

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

# Leer todos los combos (GET)
@router.get("/read_combos", response_class=HTMLResponse, tags=["Combos"])
async def read_combos(request: Request, db: Session = Depends(get_db), message: str = None):
    combos = crud.get_combos(db)
    return templates.TemplateResponse("read_combos.html", {
        "request": request, 
        "combos": combos,
        "message": message
    })

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

# Actualizar un combo (POST)
@router.post("/combos/{combo_id}/actualizar", response_class=HTMLResponse, tags=["Combos"])
async def actualizar_combo(
    request: Request,
    combo_id: int, 
    nombre: str = Form(...), 
    descripcion: str = Form(None), 
    precio: float = Form(...), 
    db: Session = Depends(get_db)
):
    try:
        # Llamar a la función de actualización desde crud.py
        combo_actualizado = crud.update_combo(
            db, 
            combo_id, 
            schemas.ComboUpdate(
                nombre=nombre, 
                descripcion=descripcion, 
                precio=precio
            )
        )
        
        if combo_actualizado is None:
            raise HTTPException(status_code=404, detail="Combo no encontrado")
        
        # Obtener los ingredientes asociados al combo actualizado
        combo_actualizado.ingredientes = crud.get_ingredientes_por_combo(db, combo_id)

        message = "Combo actualizado exitosamente"
    except Exception as e:
        message = f"Error al actualizar el combo: {str(e)}"
    
    # Devuelve la plantilla con la información del combo actualizado
    return templates.TemplateResponse("read_combos.html", {
        "request": request,
        "message": message,
        "combo": combo_actualizado  # Incluye el combo actualizado
    })

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

# Eliminar un combo (POST)
@router.post("/combos/{combo_id}/eliminar", response_class=HTMLResponse, tags=["Combos"])
async def delete_combo(combo_id: int, db: Session = Depends(get_db)):
    result = crud.delete_combo(db, combo_id)

    if result.get("status") == "success":
        return HTMLResponse(content="Combo eliminado exitosamente", status_code=200)
    else:
        return HTMLResponse(content="Error al eliminar el combo", status_code=400)
    
    
    
#======================================= RESERVAS ============================================

@router.get("/crear_reserva", response_class=HTMLResponse, tags=["Reservas"])
async def show_create_reserva_form(request: Request, db: Session = Depends(get_db)):
    clientes = crud.get_clientes(db)
    mesas = crud.get_all_mesas(db)

    print("Clientes:", clientes)  # Verificar los clientes
    print("Mesas:", mesas)  # Verificar las mesas

    return templates.TemplateResponse("crear_reserva.html", {
        "request": request,
        "clientes": clientes,
        "mesas": mesas
    })
    
#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//
    
# Crear una nueva reserva
@router.post("/crear_reserva", response_class=HTMLResponse, tags=["Reservas"])
async def create_reserva(
    request: Request,
    db: Session = Depends(get_db)
):
    form_data = await request.form()
    cliente_id = form_data.get("cliente_id")  # Asegúrate de que el nombre del campo sea cliente_id
    mesa_id = form_data.get("mesa_id")
    fecha_reserva = form_data.get("fecha_reserva")
    hora_reserva = form_data.get("hora_reserva")

    # Verificar que todos los campos requeridos estén presentes
    if None in (cliente_id, mesa_id, fecha_reserva, hora_reserva):
        return templates.TemplateResponse("crear_reserva.html", {
            "request": request,
            "message": "Por favor, completa todos los campos requeridos."
        })

    try:
        reserva_data = schemas.ReservaCreate(
            cliente_id=int(cliente_id),  # Usar cliente_id aquí
            mesa_id=int(mesa_id),
            fecha_reserva=fecha_reserva,
            hora_reserva=hora_reserva
        )
        reserva = crud.create_reserva(db, reserva_data)
        message = "Reserva creada exitosamente"
    except Exception as e:
        message = f"Error al crear la reserva: {str(e)}"

    return templates.TemplateResponse("crear_reserva.html", {
        "request": request, 
        "message": message
    })
    
#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//
    
# Leer todas las reservas
@router.get("/read_reserva", response_class=HTMLResponse, tags=["Reservas"])
async def get_reservas(request: Request, db: Session = Depends(get_db), message: str = None):
    reservas = crud.get_reservas(db)
    return templates.TemplateResponse("read_reserva.html", {
        "request": request, 
        "reservas": reservas,
        "message": message  # Pasar mensaje si existe
    })

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

# Obtener una reserva por ID (GET)
@router.get("/reservas/{reserva_id}", response_model=schemas.Reserva, tags=["Reservas"])
def get_reserva(reserva_id: int, db: Session = Depends(get_db)):
    db_reserva = crud.get_reserva(db=db, reserva_id=reserva_id)
    if db_reserva is None:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return db_reserva 

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

# Actualizar una reserva
@router.post("/reservas/{reserva_id}/actualizar", tags=["Reservas"])
async def actualizar_reserva(
    reserva_id: int,
    fecha_reserva: str = Form(...),  # Cambiado para recibir la fecha
    hora_reserva: str = Form(...),    # Cambiado para recibir la hora
    db: Session = Depends(get_db)
):
    try:
        reserva_actualizada = crud.update_reserva(
            db,
            reserva_id,
            schemas.ReservaUpdate(
                fecha=fecha_reserva,  # Usando los nuevos datos
                hora=hora_reserva
            )
        )
        if reserva_actualizada is None:
            raise HTTPException(status_code=404, detail="Reserva no encontrada")
        
        return {"mensaje": "Reserva actualizada exitosamente"}
    except Exception as e:
        print(f"Error actualizando reserva: {e}")
        raise HTTPException(status_code=500, detail="Error interno al actualizar la reserva")

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

# Eliminar una reserva (POST)
@router.post("/reservas/{reserva_id}/eliminar", response_class=HTMLResponse, tags=["Reservas"])
async def delete_reserva(reserva_id: int, db: Session = Depends(get_db)):
    result = crud.delete_reserva(db, reserva_id)

    if result.get("status") == "success":
        return HTMLResponse(content="Reserva eliminada", status_code=200)
    else:
        return HTMLResponse(content="Error al eliminar la reserva", status_code=400)
    
    
#======================================= CUENTAS DE MESAS ============================================
# Mostrar formulario para crear cuenta
@router.get("/crear_cuenta", response_class=HTMLResponse, tags=["Cuentas"])
async def show_create_cuenta_form(request: Request, db: Session = Depends(get_db)):
    mesas = crud.get_mesas_disponibles(db)  # Método para obtener las mesas disponibles
    return templates.TemplateResponse("crear_cuenta.html", {"request": request, "mesas": mesas})

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

@router.post("/crear_cuenta", response_class=HTMLResponse, tags=["Cuentas"])
async def abrir_cuenta(
    request: Request,
    db: Session = Depends(get_db)
):
    form_data = await request.form()
    mesa_id = form_data.get("mesa_id")

    # Verificar que se haya seleccionado una mesa
    if not mesa_id:
        return templates.TemplateResponse("crear_cuenta.html", {
            "request": request,
            "message": "Por favor, selecciona una mesa."
        })

    try:
        # Crear un objeto de datos para la cuenta
        cuenta_data = schemas.CuentaCreate(mesa_id=int(mesa_id))
        # Llamar a la función para abrir la cuenta
        cuenta = crud.abrir_cuenta(db, cuenta_data)

        if cuenta is None:
            # Manejar el caso en que la mesa ya tenga una cuenta abierta
            return templates.TemplateResponse("crear_cuenta.html", {
                "request": request,
                "message": "La mesa ya tiene una cuenta abierta."
            })
        
        message = "Cuenta abierta exitosamente"
    except Exception as e:
        message = f"Error al abrir la cuenta: {str(e)}"

    return templates.TemplateResponse("crear_cuenta.html", {
        "request": request,
        "message": message
    })
    
#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

# Leer todas las cuentas
@router.get("/read_cuentas", response_class=HTMLResponse, tags=["Cuentas"])
async def read_cuentas(request: Request, db: Session = Depends(get_db), message: str = None):
    cuentas = []
    combos = []
    bebidas = []

    try:
        cuentas = crud.get_cuentas(db)
        combos = crud.get_combos(db)
        bebidas = crud.get_bebidas(db)
    except Exception as e:
        print(f"Error al obtener cuentas o combos o bebidas: {e}")

    return templates.TemplateResponse("read_cuentas.html", {
        "request": request, 
        "cuentas": cuentas,
        "combos": combos,
        "bebidas": bebidas,
        "message": message
    })

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

# Obtener una cuenta por ID (GET)
@router.get("/cuentas/{cuenta_id}", response_model=schemas.Cuenta, tags=["Cuentas"])
def obtener_cuenta(cuenta_id: int, db: Session = Depends(get_db)):
    cuenta = crud.get_cuenta(db, cuenta_id)
    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada.")
    return cuenta

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

# Actualizar una cuenta
@router.post("/cuentas/{cuenta_id}/actualizar", tags=["Cuentas"])
async def actualizar_cuenta(
    cuenta_id: int, 
    id_reserva: int = Form(...), 
    db: Session = Depends(get_db)
):
    try:
        cuenta_actualizada = crud.update_cuenta(
            db, 
            cuenta_id, 
            schemas.CuentaCreate(
                id_reserva=id_reserva
            )
        )
        if cuenta_actualizada is None:
            raise HTTPException(status_code=404, detail="Cuenta no encontrada")
        return {"mensaje": "Cuenta actualizada exitosamente"}
    except Exception as e:
        print(f"Error actualizando cuenta: {e}")
        raise HTTPException(status_code=500, detail="Error interno al actualizar la cuenta")

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

# Eliminar una cuenta (POST)
@router.post("/cuentas/{cuenta_id}/eliminar", response_class=HTMLResponse, tags=["Cuentas"])
async def delete_cuenta(cuenta_id: int, db: Session = Depends(get_db)):
    result = crud.delete_cuenta(db, cuenta_id)

    if result.get("status") == "success":
        return HTMLResponse(content="Cuenta eliminada", status_code=200)
    else:
        return HTMLResponse(content="Error al eliminar la cuenta", status_code=400)
    

#======================================= PRODUCTOS ============================================
@router.post("/agregar_producto/{cuenta_id}", response_class=HTMLResponse, tags=["Cuentas"])
async def agregar_producto(
    request: Request,
    cuenta_id: int,
    productos: list[str] = Form(...),  # Recibe una lista de strings
    cantidad: int = Form(...),  # Cantidad debe ser un entero
    db: Session = Depends(get_db)
):
    print("Productos recibidos:", productos)  # Añadir línea de depuración
    print("Cantidad recibida:", cantidad)  # Añadir línea de depuración

    error_message = None
    try:
        for producto in productos:
            tipo_producto, producto_id = producto.split("_")  # Extrae tipo y ID
            print(f"Procesando: Tipo de producto - {tipo_producto}, ID - {producto_id}")  # Depuración
            detalle = crud.agregar_producto_a_cuenta(db, cuenta_id, int(producto_id), cantidad, tipo_producto)
            if detalle is None:
                error_message = f"Producto {producto_id} no encontrado o tipo inválido"
                break

        if error_message:
            return templates.TemplateResponse("read_cuentas.html", {
                "request": request,
                "error_message": error_message
            })
        else:
            return templates.TemplateResponse("read_cuentas.html", {
                "request": request,
                "message": "Productos agregados correctamente"
            })

    except Exception as e:
        print(f"Se produjo un error: {str(e)}")  # Imprimir detalles del error
        return templates.TemplateResponse("read_cuentas.html", {
            "request": request,
            "error_message": f"Error al agregar productos: {str(e)}"
        })

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//        
        
# Cerrar cuenta (POST)
@router.post("/cerrar_cuenta/{cuenta_id}", response_class=HTMLResponse, tags=["Cuentas"])
async def cerrar_cuenta_endpoint(
    cuenta_id: int,
    db: Session = Depends(get_db)
):
    cuenta = crud.cerrar_cuenta(db, cuenta_id)
    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")

    return templates.TemplateResponse("read_cuentas.html", {
        "request": request,
        "message": "Cuenta cerrada correctamente",
        "cuenta": cuenta
    })
    
#======================================= BEBIDAS ============================================
@router.get("/crear_bebida", response_class=HTMLResponse, tags=["Bebidas"])
async def show_create_bebida_form(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("crear_bebida.html", {"request": request})

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

@router.post("/crear_bebida", response_class=HTMLResponse, tags=["Bebidas"])
async def create_bebida(
    request: Request,
    nombre: str = Form(...),
    precio: float = Form(...),
    db: Session = Depends(get_db)
):
    # Aquí llamas a tu CRUD para crear la bebida en la base de datos
    nueva_bebida = schemas.BebidaCreate(nombre=nombre, precio=precio)
    crud.create_bebida(db, nueva_bebida)
    
    # Redirige a la vista de bebidas después de crear
    message = f"La bebida {nombre} fue creada correctamente."
    return templates.TemplateResponse("crear_bebida.html", {
        "request": request,
        "message": message
    })
    
#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

@router.get("/read_bebidas", response_class=HTMLResponse, tags=["Bebidas"])
async def read_bebidas(request: Request, db: Session = Depends(get_db), message: str = None):
    bebidas = crud.get_bebidas(db)  # Llama a la función para obtener las bebidas desde la base de datos
    return templates.TemplateResponse("read_bebidas.html", {
        "request": request,
        "bebidas": bebidas,
        "message": message  # Pasar mensaje si existe
    })

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

@router.get("/bebidas/{bebida_id}", response_model=schemas.Bebida ,tags=["Bebidas"])
async def get_bebida(bebida_id: int, db: Session = Depends(get_db)):
    bebida = crud.get_bebida(db, bebida_id)
    if bebida is None:
        raise HTTPException(status_code=404, detail="Bebida no encontrada")
    return bebida

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

@router.post("/bebidas/{bebida_id}/actualizar", tags=["Bebidas"])
async def update_bebida(
    bebida_id: int,
    nombre: str = Form(...),
    precio: float = Form(...),
    db: Session = Depends(get_db)
):
    try:
        bebida_actualizada = crud.update_bebida(
            db, 
            bebida_id, 
            schemas.BebidaUpdate(
                nombre=nombre,
                precio=precio
            )
        )

        if bebida_actualizada is None:
            raise HTTPException(status_code=404, detail="Bebida no encontrada")

        # Asegúrate de que 'bebida_actualizada' sea el modelo
        return {
            "mensaje": "Bebida actualizada exitosamente",
            "bebida": {
                "id": bebida_actualizada.id,  # Este debe ser el id del objeto bebida
                "nombre": bebida_actualizada.nombre,
                "precio": bebida_actualizada.precio
            }
        }
    except Exception as e:
        print(f"Error actualizando bebida: {e}")
        raise HTTPException(status_code=500, detail="Error interno al actualizar la bebida")
  
#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//
    
@router.post("/bebidas/{bebida_id}/eliminar" ,tags=["Bebidas"])
async def delete_bebida(bebida_id: int, db: Session = Depends(get_db)):
    result = crud.delete_bebida(db, bebida_id)
    if result.get("status") == "success":
        return {"message": result["message"]}
    else:
        raise HTTPException(status_code=404, detail=result["message"])
