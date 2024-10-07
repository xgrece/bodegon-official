from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import crud, schemas
from fastapi.templating import Jinja2Templates
from app.models import Cliente
from ..models import Mesa
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

@router.get("/crear_cliente", response_class=HTMLResponse)
async def show_create_cliente_form(request: Request):
    return templates.TemplateResponse("crear_cliente.html", {"request": request})

@router.post("/crear_cliente", response_class=HTMLResponse)
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

@router.get("/read_clientes", response_class=HTMLResponse)
async def read_clientes(request: Request, db: Session = Depends(get_db), message: str = None):
    clientes = crud.get_clientes(db)
    return templates.TemplateResponse("read_clientes.html", {
        "request": request, 
        "clientes": clientes,
        "message": message  # Pasar mensaje si existe
    })

# Obtener un cliente por ID (GET)
@router.get("/clientes/{cliente_id}", response_model=schemas.Cliente)
async def read_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = crud.get_cliente(db, cliente_id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente


@router.post("/clientes/{cliente_id}/actualizar")
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
    
# Eliminar un cliente (POST)
@router.post("/clientes/{cliente_id}/eliminar", response_class=HTMLResponse)
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





@router.post("/crear_mesa", response_class=HTMLResponse, tags=["Mesas"])
def create_mesa(
    request: Request,
    numero_mesa: int = Form(...),
    capacidad: int = Form(...),
    disponible: bool = Form(False),
    id_cliente: int = Form(...),  # Aquí se espera que este id sea el del cliente
    db: Session = Depends(get_db)
):
    try:
        # Verifica si los datos son válidos antes de intentar crear la mesa
        if numero_mesa <= 0 or capacidad <= 0 or id_cliente <= 0:
            raise ValueError("Los valores deben ser mayores a cero.")

        mesa_data = schemas.MesaCreate(
            numero_mesa=numero_mesa,
            capacidad=capacidad,
            disponible=disponible,
            id_cliente=id_cliente
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
        
        
        
        
        
               
@router.get("/mesas/{mesa_id}", response_model=schemas.Mesa, tags=["Mesas"])
def read_mesa(mesa_id: int, db: Session = Depends(get_db)):
    mesa = crud.get_mesa(db, mesa_id)
    if mesa is None:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    return mesa  # Devolver directamente el objeto mesa como JSON

@router.get("/read_mesas", response_class=HTMLResponse, tags=["Mesas"])
def get_all_mesas(request: Request, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    mesas = crud.get_all_mesas(db, skip=skip, limit=limit)
    return templates.TemplateResponse("read_mesas.html", {"request": request, "mesas": mesas})





@router.post("/mesas/{mesa_id}/actualizar")
async def update_mesa(
    mesa_id: int, 
    numero_mesa: int = Form(...), 
    capacidad: int = Form(...), 
    disponible: bool = Form(...), 
    db: Session = Depends(get_db)
):
    try:
        mesa_actualizada = crud.update_mesa(
            db, 
            mesa_id, 
            schemas.MesaUpdate(
                numero_mesa=numero_mesa, 
                capacidad=capacidad, 
                disponible=disponible
            )
        )
        if mesa_actualizada is None:
            raise HTTPException(status_code=404, detail="Mesa no encontrada")
        
        return {
            "mensaje": "Mesa actualizada exitosamente",
            "mesa": mesa_actualizada  # Devuelve el objeto actualizado
        }
    except Exception as e:
        print(f"Error actualizando mesa: {e}")
        raise HTTPException(status_code=500, detail="Error interno al actualizar la mesa")










@router.delete("/mesas/{mesa_id}/eliminar", response_class=HTMLResponse, tags=["Mesas"])
def delete_mesa(request: Request, mesa_id: int, db: Session = Depends(get_db)):
    crud.delete_mesa(db, mesa_id)
    return templates.TemplateResponse("read_mesas.html", {"request": request, "message": "Mesa eliminada"})

#======================================= PEDIDOS ========================================
pedidos = []

@router.post("/create_pedido", response_class=HTMLResponse, tags=["Pedidos"])
async def create_pedido(request: Request, mesa: int = Form(...), producto: str = Form(...)):
    pedidos.append({"mesa": mesa, "producto": producto})
    return templates.TemplateResponse("pedido.html", {"request": request, "pedidos": pedidos, "message": "Pedido creado exitosamente!"})

@router.get("/pedido", response_class=HTMLResponse, tags=["Pedidos"])
async def read_pedido(request: Request):
    return templates.TemplateResponse("pedido.html", {"request": request, "pedidos": pedidos})

#======================================= COMBOS ========================================
# Mostrar el formulario para crear combo (GET)
@router.get("/crear_combo", response_class=HTMLResponse)
async def show_create_combo_form(request: Request):
    return templates.TemplateResponse("crear_combo.html", {"request": request})

# Crear un combo (POST)
@router.post("/crear_combo", response_class=HTMLResponse)
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

        message = f"Combo {nombre} creado exitosamente"
    except Exception as e:
        message = f"Error al crear el combo: {str(e)}"

    return templates.TemplateResponse("crear_combo.html", {
        "request": request,
        "message": message
    })

# Obtener un combo por ID (GET)
@router.get("/combos/{combo_id}", response_model=schemas.Combo)
async def read_combo(combo_id: int, db: Session = Depends(get_db)):
    combo = crud.get_combo(db, combo_id)
    if combo is None:
        raise HTTPException(status_code=404, detail="Combo no encontrado")
    return combo

# Leer todos los combos (GET)
@router.get("/read_combos", response_class=HTMLResponse)
async def read_combos(request: Request, db: Session = Depends(get_db), message: str = None):
    combos = crud.get_combos(db)
    return templates.TemplateResponse("read_combos.html", {
        "request": request, 
        "combos": combos,
        "message": message
    })

# Actualizar un combo (POST)
@router.post("/combos/{combo_id}/actualizar", response_class=HTMLResponse)
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

# Eliminar un combo (POST)
@router.post("/combos/{combo_id}/eliminar", response_class=HTMLResponse)
async def delete_combo(combo_id: int, db: Session = Depends(get_db)):
    result = crud.delete_combo(db, combo_id)

    if result.get("status") == "success":
        return HTMLResponse(content="Combo eliminado exitosamente", status_code=200)
    else:
        return HTMLResponse(content="Error al eliminar el combo", status_code=400)
    
    
    #======================================= INGREDIENTES ========================================
