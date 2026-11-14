# Paso 1: cargar las claves del archivo .env como variables de entorno
from dotenv import load_dotenv

load_dotenv()

# Paso 2: importar el agente, el "conector" al modelo y el decorador de herramientas
from smolagents import CodeAgent, LiteLLMModel, tool

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


# Paso 5: crear el agente solo con nuestra herramienta (sin herramientas por defecto)
agent = CodeAgent(tools=[check_inventory], model=model, add_base_tools=False)

# Paso 6: darle la tarea y mostrar la respuesta final
resultado = agent.run(
    "Un cliente corporativo quiere comprar un teclado y un monitor. "
    "Usa la herramienta de inventario para revisar ambos productos. "
    "Luego, escribe el código necesario para decirme si podemos procesar el pedido completo "
    "o si hay algún quiebre de stock, y dime cuántas unidades en total podemos entregarle hoy."
)
print("\nRESULTADO FINAL:", resultado)
