from pydantic import BaseModel
from typing import List, Optional
from datetime import date, time

#===================================== S C H E M A S ========================================



# ===================================== C L I E N T E S ========================================
class ClienteBase(BaseModel):
    nombre: str
    apellido: Optional[str] = None
    email: str
    telefono: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(ClienteBase):
    pass

class Cliente(ClienteBase):
    id: int
    reservas: List['Reserva'] = []
    
    class Config:
        from_attributes = True

# ===================================== M E S A S ========================================
class MesaBase(BaseModel):
    numero_mesa: int
    capacidad: int
    disponible: bool

class MesaCreate(MesaBase):
    pass

class MesaUpdate(BaseModel):
    capacidad: int
    disponible: bool

class Mesa(MesaBase):
    id: int
    reservas: List["Reserva"] = []
    cuentas: List["Cuenta"] = []
    
    class Config:
        from_attributes = True

# ==================================== R E S E R V A S ========================================
class ReservaBase(BaseModel):
    fecha_reserva: date
    hora_reserva: time
    cliente_id: int
    mesa_id: int

class ReservaCreate(ReservaBase):
    pass

class ReservaUpdate(ReservaBase):
    pass

class Reserva(ReservaBase):
    id: int

    class Config:
        from_attributes = True

# =================================== P R O D U C T O S ========================================
class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(ProductoBase):
    pass

class Producto(ProductoBase):
    id: int
    
    class Config:
        from_attributes = True

# ================================== C O M B O S ========================================
class ComboBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float

class ComboCreate(ComboBase):
    pass

class ComboUpdate(ComboBase):
    pass

class Combo(ComboBase):
    id: int
    
    class Config:
        from_attributes = True

# ==================================== DETALLES DE CUENTA ========================================
class DetalleCuentaBase(BaseModel):
    cuenta_id: int
    producto_id: int
    cantidad: int
    precio_unitario: float
    subtotal: float

class DetalleCuentaCreate(DetalleCuentaBase):
    pass

class DetalleCuenta(DetalleCuentaBase):
    id: int
    
    class Config:
        from_attributes = True

# =================================== CUENTAS =============================================
class CuentaBase(BaseModel):
    mesa_id: int
    fecha_apertura: Optional[date] = None
    estado: str = "abierta"
    total: Optional[float] = 0.0

class CuentaCreate(CuentaBase):
    pass

class Cuenta(CuentaBase):
    id: int
    detalles: List[DetalleCuenta] = []
    
    class Config:
        from_attributes = True

# ================================ INGREDIENTES ========================================
class IngredienteBase(BaseModel):
    nombre: str

class IngredienteCreate(IngredienteBase):
    pass

class IngredienteUpdate(IngredienteBase):
    pass

class Ingrediente(IngredienteBase):
    id: int
    
    class Config:
        from_attributes = True

#================================== P E D I D O S ========================================
# Base schema for Pedido
class PedidoBase(BaseModel):
    cliente_id: int
    mesa_id: int
    combo_id: int
    fecha_pedido: Optional[date] = None
    total_pedido: float

# Schema for creating a Pedido
class PedidoCreate(PedidoBase):
    pass

# Schema for updating a Pedido (optional fields for partial update)
class PedidoUpdate(BaseModel):
    cliente_id: Optional[int] = None
    mesa_id: Optional[int] = None
    combo_id: Optional[int] = None
    fecha_pedido: Optional[date] = None
    total_pedido: Optional[float] = None

# Schema for reading Pedido (includes id)
class Pedido(PedidoBase):
    id: int

    class Config:
        from_attributes = True
        
        
#================================== B E B I D A S ========================================
from pydantic import BaseModel

class BebidaBase(BaseModel):
    nombre: str
    precio: float

class BebidaCreate(BebidaBase):
    pass

class BebidaUpdate(BebidaBase):
    pass

class Bebida(BebidaBase):
    id: int

    class Config:
        from_attributes = True