from pydantic import BaseModel
from typing import List, Optional
from datetime import date, time

#===================================== S C H E M A S ========================================



#==================================== C L I E N T E S ========================================
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
    pedidos: List['Pedido'] = []
    class Config:
        from_attributes = True

#===================================== M E S A S ========================================
class MesaBase(BaseModel):
    numero_mesa: int
    capacidad: int
    disponible: bool
    

class MesaCreate(MesaBase):
    id_cliente: int

class MesaUpdate(MesaBase):
    pass

class Mesa(MesaBase):
    id: int
    id_cliente: int
    reservas: List["Reserva"] = []
    pedidos: List["Pedido"] = []
    class Config:
        from_attributes = True

#===================================== R E S E R V A S ========================================
class ReservaBase(BaseModel):
    fecha: date
    hora: time
    cliente_id: int
    mesa_id: int

class ReservaCreate(ReservaBase):
    pass

class ReservaUpdate(ReservaBase):
    pass

class Reserva(ReservaBase):
    id: int
    cliente: Cliente
    mesa: 'Mesa'
    class Config:
        from_attributes = True

#====================================== C O M B O S ========================================
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

#================================== P E D I D O S ========================================
class PedidoBase(BaseModel):
    cantidad: int
    producto: str
    # Puedes agregar más campos si tienes relaciones, por ejemplo, cliente_id, combo_id, etc.

class PedidoCreate(PedidoBase):
    pass

class PedidoUpdate(PedidoBase):
    pass

class Pedido(PedidoBase):
    id: int
    # Relaciones, si es necesario
    cliente_id: int  # si está relacionado con cliente, por ejemplo
    combo_id: Optional[int] = None  # si aplica
    class Config:
        from_attributes = True

#============================== METODOS PAGO ========================================
class MetodoPagoBase(BaseModel):
    nombre: str

class MetodoPagoCreate(MetodoPagoBase):
    pass

class MetodoPagoUpdate(MetodoPagoBase):
    pass

class MetodoPago(MetodoPagoBase):
    id: int
    class Config:
        from_attributes = True

#=================================== P A G O S ========================================
class PagoBase(BaseModel):
    monto: float
    fecha: date
    metodo_pago_id: int

class PagoCreate(PagoBase):
    pass

class PagoUpdate(PagoBase):
    pass

class Pago(PagoBase):
    id: int
    class Config:
        from_attributes = True

#=========================== E M P L E A D O S ========================================
class EmpleadoBase(BaseModel):
    nombre: str
    email: str
    telefono: Optional[str] = None
    rol: str

class EmpleadoCreate(EmpleadoBase):
    pass

class EmpleadoUpdate(EmpleadoBase):
    pass

class Empleado(EmpleadoBase):
    id: int
    class Config:
        from_attributes = True


#============================= P R O V E E D O R E S ========================================
class ProveedorBase(BaseModel):
    nombre: str
    contacto: Optional[str] = None
    telefono: Optional[str] = None
    email: str
    direccion: Optional[str] = None

class ProveedorCreate(ProveedorBase):
    pass

class ProveedorUpdate(ProveedorBase):
    pass

class Proveedor(ProveedorBase):
    id: int
    inventario: List['Inventario'] = []
    class Config:
        from_attributes = True
        
#=================================== I N V E N T A R I O ========================================
class InventarioBase(BaseModel):
    producto: str
    cantidad: int
    proveedor_id: int

class InventarioCreate(InventarioBase):
    pass

class InventarioUpdate(InventarioBase):
    pass

class Inventario(InventarioBase):
    id: int
    proveedor: Proveedor
    class Config:
        from_attributes = True
        
#---------------------- U S U A R I O ----------------------------------------------

