# curso-ai-agents

Curso práctico para aprender a construir **agentes de IA y sistemas multi-agente** con la librería [`smolagents`](https://github.com/huggingface/smolagents) de Hugging Face, aplicando *Vibe Coding*: el desarrollador define la arquitectura y la intención, y delega la sintaxis a un asistente de IA.

## Estado actual

**Unidad 3 completada:** un agente Code-Act con una herramienta personalizada de inventario.

| Unidad | Tema | Concepto clave |
|---|---|---|
| 1 | Primer agente | `CodeAgent` + modelo: el agente escribe y ejecuta Python para resolver una tarea (Fibonacci) |
| 2 | Acceso a internet | `DuckDuckGoSearchTool`: el agente busca datos actuales (precios de acciones) |
| 3 | Custom Tools | `@tool`: herramienta propia `check_inventory` con una base de datos simulada |

## Arquitectura

```
src/
└── main_agent.py   # Agente principal (modelo + herramientas + tarea)
```

El agente se compone de tres piezas:

| Pieza | Implementación | Rol |
|---|---|---|
| Modelo ("cerebro") | `LiteLLMModel(model_id="anthropic/claude-haiku-5-5")` | Razona y decide qué hacer |
| Agente ("cuerpo") | `CodeAgent` | Convierte el razonamiento en código Python y lo ejecuta |
| Herramientas ("manos") | `check_inventory` (decorada con `@tool`) | Acciones que el agente puede invocar |

### Patrón Code-Act

`CodeAgent` no responde con texto ni con JSON: **escribe código Python** en cada paso. Ese código llama a las herramientas como si fueran funciones normales, y el agente lee lo que imprime. El ciclo se repite hasta que llama a `final_answer(...)`:

```
pensar → escribir código → ejecutar (llamar herramientas) → observar → … → final_answer
```

### Custom Tools

Una función decorada con `@tool` se convierte en herramienta. **El agente no ve su código interno**, solo:

- el **nombre** de la función,
- los **tipos** de los argumentos y del retorno,
- el **docstring**, con su sección `Args:`, que es obligatoria.

El docstring funciona como manual de uso: si es pobre, el agente usará mal la herramienta.

### Decisiones de diseño

- **`add_base_tools=False`:** el agente solo tiene las herramientas que le damos de forma explícita. Así hay más control y menos superficie de error.
- **Modelo Haiku:** es suficiente para los ejercicios del curso y es más barato y rápido. Se puede cambiar editando una sola línea (`model_id`).

## Requisitos

- Python 3.10+ (desarrollado con 3.14)
- Clave de API de Anthropic (y, de forma opcional, de OpenAI o Hugging Face)

Dependencias principales (lista completa en `requirements.txt`):

| Paquete | Uso |
|---|---|
| `smolagents` | Framework de agentes |
| `litellm` | Conector para `LiteLLMModel` (modelos de Anthropic) |
| `ddgs` | Búsqueda web para `DuckDuckGoSearchTool` |
| `anthropic`, `openai` | SDKs de los proveedores de modelos |
| `python-dotenv` | Carga de claves desde `.env` |

## Instalación

```bash
# 1. Crear y activar el entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# 2. Instalar dependencias
pip install -r requirements.txt
```

## Configuración

Crea un archivo `.env` en la raíz y pega tus claves después del `=`, sin comillas:

```
ANTHROPIC_API_KEY=
OPENAI_API_KEY=
HF_TOKEN=
```

> `.env` y `.venv/` están en `.gitignore`. **Nunca subas tus claves al repositorio.**

## Uso

```bash
source .venv/bin/activate
python src/main_agent.py
```

O sin activar el entorno:

```bash
.venv/bin/python src/main_agent.py
```

En la consola verás cada paso del agente: el código que escribe, lo que se ejecuta y la respuesta final.

## Lecciones aprendidas

- **Errores de dependencias:** `LiteLLMModel` necesita `smolagents[litellm]` y la búsqueda web necesita `ddgs` (`smolagents[toolkit]`). Lee siempre la última línea del error.
- **Herramientas externas poco fiables:** DuckDuckGo puede devolver "No results found" si recibe muchas consultas seguidas. Sirve para aprender, pero no para producción.
- **Precisión del prompt:** el agente hace lo que dices, no lo que quieres decir. En la Unidad 3, al no indicar cantidades del pedido, sumó todo el stock (42) en lugar de las unidades pedidas (1).

## Próximos pasos

- [ ] Ajustar el reto de inventario con cantidades explícitas
- [ ] Combinar varias herramientas en un mismo agente
- [ ] Sistemas multi-agente: un agente gestor que delega en agentes especializados
