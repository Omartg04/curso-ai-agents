# Paso 1: cargar las claves del archivo .env como variables de entorno
from dotenv import load_dotenv

load_dotenv()

# Paso 2: importar el agente, el "conector" al modelo y el decorador de herramientas
# Nota: `ManagedAgent` se eliminó de smolagents. Ahora el especialista es un
# CodeAgent con `name` + `description`, y se pasa al manager en `managed_agents`.
from smolagents import CodeAgent, DuckDuckGoSearchTool, LiteLLMModel, tool

# Paso 3: elegir el modelo (el "cerebro" del agente).
# LiteLLM lee ANTHROPIC_API_KEY automáticamente del entorno.
model = LiteLLMModel(model_id="anthropic/claude-haiku-5-5")


# Paso 4: crear nuestra propia herramienta.
# @tool convierte una función normal en una herramienta para el agente.
# El agente NO ve el código de dentro: solo ve el nombre, los tipos y el docstring.
@tool
def check_inventory(product_name: str) -> str:
    """
    Consulta el inventario del almacén y devuelve cuántas unidades hay disponibles
    de un producto. Si el producto no existe en el catálogo, lo indica.

    Args:
        product_name: Nombre del producto a consultar, en español y en singular
            (por ejemplo: "laptop", "teclado" o "monitor").
    """
    # Base de datos simulada: producto -> unidades en stock
    inventario = {"laptop": 15, "teclado": 0, "monitor": 42}

    nombre = product_name.strip().lower()
    if nombre not in inventario:
        return f"El producto '{product_name}' no existe en el inventario."
    return f"Producto '{nombre}': {inventario[nombre]} unidades disponibles."


# Paso 5: el "Especialista Web". El name y la description son lo que el
# manager ve de él (igual que el docstring de una herramienta).
web_agent = CodeAgent(
    tools=[DuckDuckGoSearchTool()],
    model=model,
    add_base_tools=False,
    name="web_searcher",
    description="Agente especialista en buscar información actualizada en internet (precios, noticias, datos).",
)

# Paso 6: el "Manager". Usa el inventario directamente y delega en web_searcher.
manager_agent = CodeAgent(
    tools=[check_inventory],
    model=model,
    add_base_tools=False,
    managed_agents=[web_agent],
)

# Paso 7: el reto
resultado = manager_agent.run(
    "Un cliente quiere comprar exactamente 1 teclado y 1 monitor. Usa el inventario para decirme "
    "si podemos entregarle los 2 artículos, o solo 1, o ninguno. Además, el cliente pagará con "
    "acciones de Apple; pide a tu especialista 'web_searcher' que busque el precio actual de la "
    "acción de AAPL. Entrégame un reporte final detallando la disponibilidad y el precio de la acción."
)
print("\nRESULTADO FINAL:", resultado)
