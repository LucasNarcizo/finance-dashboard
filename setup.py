from setuptools import setup, find_packages

setup(
    name="FinançasDashboard",
    version="0.1.0",
    # find_packages() vai encontrar automaticamente sua pasta 'src'
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "pandas",
        "plotly",
        "supabase",
        "python-dotenv",
        "requests",
    ],
)