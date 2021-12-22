from setuptools import find_packages, setup


setup(
    name="db_lib",
    packages=find_packages(),
    version="0.1.1",
    description="Realtime project",
    author="Andrei Ponomarev",
    install_requires=["alembic==1.7.4", "fastapi-sqlalchemy==0.2.1", "psycopg2-binary==2.9.1", "python-dotenv==0.19.2"],
    license="MIT",
)