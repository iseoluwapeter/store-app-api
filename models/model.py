from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from database import Base
import datetime


class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key = True, index = True)
    name = Column(String)
    address = Column(String)
    phone = Column(Integer)
    email = Column(String)
    other_details = Column(String)

class Role(Base):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True, index= True)
    name = Column(String)
    desc = Column(String)

    staff_members = relationship("Staff", back_populates="role")

class Staff(Base):
    __tablename__ = "staff"
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    address=  Column(String)
    phone = Column(String)
    email= Column(String)
    username = Column(String, unique=True)
    password = Column(String, unique=True)
    role_id = Column(Integer, ForeignKey("role.id"))  

    role = relationship("Role", back_populates="staff_members")
    customers = relationship("Customer", back_populates="staff") 


class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    address = Column(String)
    phone = Column(String)
    email = Column(String, unique=True)
    staff_id = Column(Integer, ForeignKey("staff.id"))

    staff = relationship("Staff", back_populates="customers")
    orders = relationship("Order", back_populates="customer")

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)

    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    desc = Column(String)
    unit = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
    status = Column(Integer)
    other_details = Column(String)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
 

    category = relationship("Category", back_populates="products")
    orderdetails = relationship("OrderDetail", back_populates="product")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    date_of_order = Column(DateTime)
    order_details = Column(String)
    customer_id = Column(Integer, ForeignKey("customers.id"))

    customer = relationship("Customer", back_populates="orders")
    orderdetails = relationship("OrderDetail", back_populates="order")


class OrderDetail(Base):
    __tablename__ = "orderdetail"
    id= Column(Integer, primary_key=True, index=True)
    unit_price= Column(Float)
    size = Column(Integer)
    quantity = Column(Integer)
    discount = Column(Integer)
    total = Column(Float)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    product_id = Column(Integer, ForeignKey("products.id"))  
    order_id = Column(Integer, ForeignKey("orders.id"))
    bill_number = Column(Integer, ForeignKey("payment.bill_number"))

    product = relationship("Product", back_populates="orderdetails")
    payment = relationship("Payment", back_populates="orderdetails")
    order = relationship("Order", back_populates="orderdetails")

class Payment(Base):
    __tablename__ ="payment"
    bill_number = Column(Integer, primary_key=True, index=True)
    payment_type = Column(String)
    other_details = Column(String) 

    orderdetails = relationship("OrderDetail", back_populates="payment") 
