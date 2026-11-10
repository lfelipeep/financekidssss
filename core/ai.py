import os
from openai import OpenAI

# Se prueban en orden. Si uno falla o está saturado, pasa al siguiente.
# Los proveedores sin key configurada se saltan solos.
PROVEEDORES = [
    ("groq", "https://api.groq.com/openai/v1", "GROQ_API_KEY", "openai/gpt-oss-120b"),
    ("gemini", "https://generativelanguage.googleapis.com/v1beta/openai/", "GEMINI_API_KEY", "gemini-3.8-flash"),
    ("gemini", "https://generativelanguage.googleapis.com/v1beta/openai/", "GEMINI_API_KEY", "gemini-3.6-flash"),
]

SYSTEM = """Eres un tutor de finanzas para niños de 8 a 12 años.
Explica con ejemplos simples y tono amable, en máximo 4 frases.
Solo hablas de dinero, ahorro y presupuesto.
Si preguntan otra cosa, redirige con cortesía."""


def preguntar_tutor(pregunta):
    for nombre, url, key_env, modelo in PROVEEDORES:
        key = os.environ.get(key_env)
        if not key:
            continue
        try:
            client = OpenAI(base_url=url, api_key=key, timeout=15, max_retries=0)
            r = client.chat.completions.create(
                model=modelo,
                max_tokens=1500,
                messages=[
                    {"role": "system", "content": SYSTEM},
                    {"role": "user", "content": pregunta},
                ],
            )
            texto = r.choices[0].message.content
            if texto:
                return texto
        except Exception as e:
            print(f"ERROR IA ({nombre} / {modelo}):", repr(e))
            continue

    return "Ahora mismo hay mucha gente usando el tutor. ¡Intenta de nuevo en un ratito!"