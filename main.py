from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import customer, role, staff, category,  order, supplier, product, payment, orderdetails, auth
from database import Base, engine
import os

app = FastAPI()



frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5174")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, "http://localhost:5174"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"]
)

app.include_router(role.role_router, prefix="/role", tags=["role"])
app.include_router(supplier.supplier_router, prefix="/supplier", tags=["supplier"])
app.include_router(staff.staff_router, prefix="/staff", tags=["staff"])
app.include_router(customer.customer_router, prefix="/customer", tags=["customers"])
app.include_router(category.category_router, prefix="/category", tags=["category"])
app.include_router(order.order_router, prefix="/order", tags=["order"])
app.include_router(product.product_router, prefix="/product", tags=["product"])
app.include_router(payment.payment_router, prefix="/payment", tags=["payment"])
app.include_router(orderdetails.orderdetails_router, prefix="/order_details", tags=["order_details"])
app.include_router(auth.auth_router, prefix="/auth_router", tags=["auth_router"])



