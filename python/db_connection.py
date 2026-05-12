from sqlalchemy import create_engine

# Create and expose engine
engine = create_engine(
    "mysql+pymysql://root:Kitty%40123@localhost:3306/sales_analytics"
)