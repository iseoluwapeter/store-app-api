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

    staff = relationship("Staff", back_populates="role")

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

    role = relationship("Role", back_populates="staff")
    customer = relationship("Customer", back_populates="staff") 


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
    orders = relationship("Order", back_populates="customers")

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
 

# #     # products = relationship("Product", back_populates="category")

# class Product(Base):
#     __tablename__ = "products"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
#     desc = Column(String)
#     price = Column(Float)
#     stock = Column(Integer)
#     catgory_id = Column(Integer, ForeignKey("categories.id"))
 

# #     # category = relationship("Category", back_populates="products")
# #     # orders = relationship("Order", back_populates="product")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    date_of_order = Column(DateTime)
    order_details = Column(String)
    customer_id = Column(Integer, ForeignKey("customers.id"))

    customer = relationship("Customer", back_populates=("orders"))
# #     # customer = relationship("Customer", back_populates="orders")
# #     # product = relationship("Product", back_populates="orders")

# class OrderDetail(Base):
#     __tablename__ = "orderdetail"
#     id= Column(Integer, primary_key=True, index=True)
#     unit_price= Column(Float)
#     size = Column(Integer,)
#     Quantity = Column(Integer)
#     Discount = Column(Integer)
#     Total = Column(Integer)
#     date = Column(DateTime, default=datetime.datetime.utcnow)
#     product_id = Column(Integer, ForeignKey("products.id"))  
#     order_id = Column(Integer, ForeignKey("orders.id"))

# class Payment(Base):
#     __tablename__ ="payment"
#     bill_number = Column(Integer, primary_key=True, index=True)
#     payment_type = Column(String)
#     other_details = Column(String)  
