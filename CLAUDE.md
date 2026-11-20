# CLAUDE.md

## Propósito
Curso práctico de AI Agents y Vibe Coding. El usuario está aprendiendo: define la arquitectura y la intención, y Claude escribe la sintaxis. Claude actúa como ingeniero de software principal y mentor.

- Responde siempre en **español** y explica de forma simple.
- Tras ejecutar un agente, analiza la salida de la consola: cómo razonó el agente, qué herramientas usó y si el resultado es correcto (señala los fallos de lógica aunque el código "funcione").

## Stack
- Python 3.14, con el entorno virtual en `.venv/`
- `smolagents` (Hugging Face) como framework de agentes
- `LiteLLMModel` para conectarse a Anthropic (requiere `smolagents[litellm]`)
- `python-dotenv` para cargar las claves desde `.env` (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `HF_TOKEN`)

## Arquitectura
- **Patrón Code-Act:** `CodeAgent` escribe y ejecuta Python en cada paso; llama a las herramientas como funciones y termina con `final_answer(...)`.
- **Custom Tools:** funciones con `@tool`. El docstring con sección `Args:` es obligatorio, porque es lo único que el agente ve de la herramienta.
- **Delegación a agentes especialistas (Unidad 4):** un agente gestor (manager) delega tareas en agentes especialistas. El especialista es un `CodeAgent` con `name` y `description`, y se pasa al manager con `managed_agents=[...]`. `ManagedAgent` está obsoleto: no lo uses.
- Usa `add_base_tools=False` por defecto: el agente solo recibe las herramientas que se le pasan de forma explícita.

## Notas de entorno
- **Modelo por defecto:** `LiteLLMModel(model_id="anthropic/claude-haiku-5-5")`. No uses modelos más grandes salvo que el usuario lo pida.
- **Ejecutar:** `.venv/bin/python src/main_agent.py`
- **Logs de ejecución:** cada ejecución de un agente se guarda en un archivo nuevo de `logs/`, con el nombre `logs/unidad<N>_<NN>_<descripcion>.txt` (por ejemplo, `logs/unidad4_02_visitwebpage.txt`). Usa `> archivo 2>&1` para guardar también los errores. No sobrescribas los logs anteriores. El usuario usa estos archivos como apuntes del curso y se suben a git.
- **Instalar paquetes:** `.venv/bin/pip install ...` y luego regenerar `.venv/bin/pip freeze > requirements.txt`
- `DuckDuckGoSearchTool` necesita `ddgs` (`smolagents[toolkit]`) y a veces falla con "No results found" por límite de uso: es un problema transitorio, no un bug del código.
- `.env` y `.venv/` están en `.gitignore`. Nunca muestres ni subas las claves.

## Reglas de Vibe Coding
- **Antes de escribir código, explica siempre brevemente tu razonamiento:** qué vas a cambiar y por qué.
- Si una instrucción del usuario usa una API o un modelo obsoleto, avísale y usa la alternativa vigente.
- Haz commit y push solo cuando el usuario lo pida.

## Progreso del curso
- **Unidad 4 completada:** sistema multi-agente funcional. El manager (`CodeAgent` con la herramienta `check_inventory`) consulta el stock y delega la búsqueda web en el especialista `web_searcher` (`DuckDuckGoSearchTool` + `VisitWebpageTool`), que abre las páginas y lee los datos actualizados. Las ejecuciones están en `logs/unidad4_01_multiagente.txt` y `logs/unidad4_02_visitwebpage.txt`.
