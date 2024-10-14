from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship, declarative_base, Session
from datetime import datetime
from .database import Base



#==================================== C L I E N T E S ========================================
class Cliente(Base):
    __tablename__ = 'clientes'
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(250), index=True)
    apellido = Column(String, index=True)
    email = Column(String(250), unique=True, index=True)
    telefono = Column(String(15), index=True)

    # Relaciones
    reservas = relationship("Reserva", back_populates="cliente")
    pedidos = relationship("Pedido", back_populates="cliente")


    # Métodos CRUD
    @classmethod
    def create(cls, session: Session, **kwargs):
        new_cliente = cls(**kwargs)
        session.add(new_cliente)
        session.commit()
        session.refresh(new_cliente)
        return new_cliente

    @classmethod
    def read(cls, session: Session, cliente_id: int):
        return session.query(cls).filter(cls.id == cliente_id).first()

    @classmethod
    def read_all(cls, session: Session, skip: int = 0, limit: int = 10):
        return session.query(cls).offset(skip).limit(limit).all()

    def update(self, session: Session, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        session.commit()
        session.refresh(self)
        return self

    def delete(self, session: Session):
        session.delete(self)
        session.commit() 

#===================================== M E S A S ========================================
class Mesa(Base):
    __tablename__ = 'mesas'
    
    id = Column(Integer, primary_key=True, index=True)
    numero_mesa = Column(Integer, unique=True, index=True)
    capacidad = Column(Integer)
    disponible = Column(Boolean, default=True)

    #Relaciones
    reservas = relationship("Reserva", back_populates="mesa")
    pedidos = relationship("Pedido", back_populates="mesa")
    
    
    
    # Métodos CRUD
    @classmethod
    def create(cls, session: Session, **kwargs):
        new_mesa = cls(**kwargs)
        session.add(new_mesa)
        session.commit()
        session.refresh(new_mesa)
        return new_mesa

    @classmethod
    def read(cls, session: Session, mesa_id: int):
        return session.query(cls).filter(cls.id == mesa_id).first()

    @classmethod
    def read_all(cls, session: Session, skip: int = 0, limit: int = 10):
        return session.query(cls).offset(skip).limit(limit).all()

    def update(self, session: Session, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        session.commit()
        session.refresh(self)
        return self

    def delete(self, session: Session):
        session.delete(self)
        session.commit()

#===================================== R E S E R V A S ========================================
class Reserva(Base):
    __tablename__ = 'reservas'
    id = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey('clientes.id'))
    mesa_id = Column(Integer, ForeignKey('mesas.id'))
    fecha_reserva = Column(DateTime, default=datetime.utcnow)
    hora_reserva = Column(String(10))
    
    #Relaciones
    cliente = relationship("Cliente", back_populates="reservas")
    mesa = relationship("Mesa", back_populates="reservas")
    cuenta = relationship("Cuenta", back_populates="reservas")
    
    # Métodos CRUD
    @classmethod
    def create(cls, session: Session, **kwargs):
        new_reserva = cls(**kwargs)
        session.add(new_reserva)
        session.commit()
        session.refresh(new_reserva)
        return new_reserva

    @classmethod
    def read(cls, session: Session, reserva_id: int):
        return session.query(cls).filter(cls.id == reserva_id).first()

    @classmethod
    def read_all(cls, session: Session, skip: int = 0, limit: int = 10):
        return session.query(cls).offset(skip).limit(limit).all()

    def update(self, session: Session, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        session.commit()
        session.refresh(self)
        return self

    def delete(self, session: Session):
        session.delete(self)
        session.commit()

#====================================== C O M B O S ========================================
class Combo(Base):
    __tablename__ = 'combos'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(250), index=True)
    descripcion = Column(String(500))
    precio = Column(Float)
    #Relaciones
    pedidos = relationship("Pedido", back_populates="combo")
    ingredientes = relationship("Ingrediente", back_populates="combo")
    
    # Métodos CRUD
    @classmethod
    def create(cls, session: Session, **kwargs):
        new_combo = cls(**kwargs)
        session.add(new_combo)
        session.commit()
        session.refresh(new_combo)
        return new_combo

    @classmethod
    def read(cls, session: Session, obj_id: int):
        return session.query(cls).filter(cls.id == obj_id).first()

    @classmethod
    def read_all(cls, session: Session, skip: int = 0, limit: int = 10):
        return session.query(cls).offset(skip).limit(limit).all()

    def update(self, session: Session, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        session.commit()
        session.refresh(self)
        return self

    def delete(self, session: Session):
        session.delete(self)
        session.commit()

#================================== P E D I D O S ========================================
class Pedido(Base):
    __tablename__ = 'pedidos'
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    mesa_id = Column(Integer, ForeignKey('mesas.id'))
    combo_id = Column(Integer, ForeignKey('combos.id'))
    fecha_pedido = Column(DateTime, default=datetime.utcnow)
    total_pedido = Column(Float)
    
    #Relaciones
    cliente = relationship("Cliente", back_populates="pedidos")
    mesa = relationship("Mesa", back_populates="pedidos")
    combo = relationship("Combo", back_populates="pedidos")
    pagos = relationship("Pago", back_populates="pedido")
    
    # Métodos CRUD
    @classmethod
    def create(cls, session: Session, **kwargs):
        new_pedido = cls(**kwargs)
        session.add(new_pedido)
        session.commit()
        session.refresh(new_pedido)
        return new_pedido

    @classmethod
    def read(cls, session: Session, pedido_id: int):
        return session.query(cls).filter(cls.id == pedido_id).first()

    @classmethod
    def read_all(cls, session: Session, skip: int = 0, limit: int = 10):
        return session.query(cls).offset(skip).limit(limit).all()

    def update(self, session: Session, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        session.commit()
        session.refresh(self)
        return self

    def delete(self, session: Session):
        session.delete(self)
        session.commit()

#============================== METODOS PAGO ========================================
class MetodoPago(Base):
    __tablename__ = 'metodos_pago'
    id = Column(Integer, primary_key=True, index=True)
    tipo_metodo = Column(String(50), index=True)
    
    #Relaciones
    pagos = relationship("Pago", back_populates="metodo_pago")
    
    # Métodos CRUD
    @classmethod
    def create(cls, session: Session, **kwargs):
        new_metodo_pago = cls(**kwargs)
        session.add(new_metodo_pago)
        session.commit()
        session.refresh(new_metodo_pago)
        return new_metodo_pago

    @classmethod
    def read(cls, session: Session, obj_id: int):
        return session.query(cls).filter(cls.id == obj_id).first()

    @classmethod
    def read_all(cls, session: Session, skip: int = 0, limit: int = 10):
        return session.query(cls).offset(skip).limit(limit).all()

    def update(self, session: Session, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        session.commit()
        session.refresh(self)
        return self

    def delete(self, session: Session):
        session.delete(self)
        session.commit()

#=================================== P A G O S ========================================
class Pago(Base):
    __tablename__ = 'pagos'
    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey('pedidos.id'))
    metodo_pago_id = Column(Integer, ForeignKey('metodos_pago.id'))
    monto = Column(Float)
    fecha_pago = Column(DateTime, default=datetime.utcnow)
    
    #Relaciones
    pedido = relationship("Pedido", back_populates="pagos")
    metodo_pago = relationship("MetodoPago", back_populates="pagos")
    
    # Métodos CRUD
    @classmethod
    def create(cls, session: Session, **kwargs):
        new_pago = cls(**kwargs)
        session.add(new_pago)
        session.commit()
        session.refresh(new_pago)
        return new_pago

    @classmethod
    def read(cls, session: Session, obj_id: int):
        return session.query(cls).filter(cls.id == obj_id).first()

    @classmethod
    def read_all(cls, session: Session, skip: int = 0, limit: int = 10):
        return session.query(cls).offset(skip).limit(limit).all()

    def update(self, session: Session, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        session.commit()
        session.refresh(self)
        return self

    def delete(self, session: Session):
        session.delete(self)
        session.commit()

#=========================== E M P L E A D O S ========================================
class Empleado(Base):
    __tablename__ = 'empleados'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(250), index=True)
    puesto = Column(String(100))
    email = Column(String(250), unique=True, index=True)
    telefono = Column(String(15), index=True)
    
    # Métodos CRUD
    @classmethod
    def create(cls, session: Session, **kwargs):
        new_empleado = cls(**kwargs)
        session.add(new_empleado)
        session.commit()
        session.refresh(new_empleado)
        return new_empleado

    @classmethod
    def read(cls, session: Session, obj_id: int):
        return session.query(cls).filter(cls.id == obj_id).first()

    @classmethod
    def read_all(cls, session: Session, skip: int = 0, limit: int = 10):
        return session.query(cls).offset(skip).limit(limit).all()

    def update(self, session: Session, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        session.commit()
        session.refresh(self)
        return self

    def delete(self, session: Session):
        session.delete(self)
        session.commit()

#============================= P R O V E E D O R E S ========================================
class Proveedor(Base):
    __tablename__ = 'proveedores'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(250), index=True)
    contacto = Column(String(250))
    telefono = Column(String(15))
    email = Column(String(250), unique=True, index=True)
    direccion = Column(String(500))
    
    #Relaciones
    inventario = relationship("Inventario", back_populates="proveedor")
    
    # Métodos CRUD
    @classmethod
    def create(cls, session: Session, **kwargs):
        new_proveedor = cls(**kwargs)
        session.add(new_proveedor)
        session.commit()
        session.refresh(new_proveedor)
        return new_proveedor

    @classmethod
    def read(cls, session: Session, proveedor_id: int):
        return session.query(cls).filter(cls.id == proveedor_id).first()

    @classmethod
    def read_all(cls, session: Session, skip: int = 0, limit: int = 10):
        return session.query(cls).offset(skip).limit(limit).all()

    def update(self, session: Session, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        session.commit()
        session.refresh(self)
        return self

    def delete(self, session: Session):
        session.delete(self)
        session.commit()

#=================================== I N V E N T A R I O ========================================
class Inventario(Base):
    __tablename__ = 'inventario'
    id = Column(Integer, primary_key=True, index=True)
    producto = Column(String(250))
    cantidad = Column(Integer)
    proveedor_id = Column(Integer, ForeignKey('proveedores.id'))
    
    #Relaciones
    proveedor = relationship("Proveedor", back_populates="inventario")
    
    # Métodos CRUD
    @classmethod
    def create(cls, session: Session, **kwargs):
        new_inventario = cls(**kwargs)
        session.add(new_inventario)
        session.commit()
        session.refresh(new_inventario)
        return new_inventario

    @classmethod
    def read(cls, session: Session, inventario_id: int):
        return session.query(cls).filter(cls.id == inventario_id).first()

    @classmethod
    def read_all(cls, session: Session, skip: int = 0, limit: int = 10):
        return session.query(cls).offset(skip).limit(limit).all()

    def update(self, session: Session, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        session.commit()
        session.refresh(self)
        return self

    def delete(self, session: Session):
        session.delete(self)
        session.commit()
        
#---------------------- U S U A R I O ----------------------------------------------

#============================== INGREDIENTES ========================================
class Ingrediente(Base):
    __tablename__ = "ingredientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(250), index=True)
    combo_id = Column(Integer, ForeignKey("combos.id"))

#Relaciones
    combo = relationship("Combo", back_populates="ingredientes")
    
#============================== CUENTAS ========================================
class Cuenta(Base):
    __tablename__ = 'cuentas'
    id = Column(Integer, primary_key=True, index=True)
    total = Column(Float, nullable=False)
    metodo_pago = Column(String(50), nullable=True)
    reserva_id = Column(Integer, ForeignKey('reservas.id'), nullable=False)

    #Relaciones
    reservas = relationship("Reserva", back_populates="cuenta")
    