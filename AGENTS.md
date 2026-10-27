# AGENTS.md

## Objetivo del proyecto

Backend **muy simple** para un chatbot de atención al cliente:

1. Recibir mensajes de WhatsApp (y quizá otros canales, como email).
2. Pasarlos a una IA para generar la respuesta.
3. Enviar la respuesta y guardar el estado del mensaje.

La simplicidad es un requisito: no añadir capas, librerías ni abstracciones que el proyecto no necesite todavía.

## Objetivo de aprendizaje

El autor vuelve a programar después de años con PHP (algo de POO, poca arquitectura). Este proyecto sirve para **entender cada pieza** y subir de nivel en backend. Por eso:

- **Explica siempre el porqué** de cada decisión, no solo el qué.
- **Usa analogías con PHP / Laravel** cuando ayuden (por ejemplo: interfaz de repositorio ↔ `interface` + binding en `AppServiceProvider`; `Depends` de FastAPI ↔ inyección por constructor del contenedor de Laravel; Pydantic ↔ Form Requests).
- Señala los errores típicos y las alternativas que se descartaron, en pocas líneas.

## Forma de trabajar

- **Poco código cada vez.** Un concepto o una pieza por paso; nunca generar muchos ficheros de golpe.
- Antes de escribir, explica brevemente qué se va a hacer y por qué.
- Cuando tenga sentido, propón que el autor escriba el código él mismo y ofrece revisarlo.
- Después de cada paso, comprueba que funciona (arrancar el servidor, probar con curl, tests) y explica el resultado.
- Responde en español.

## Arquitectura: DDD práctico, sin dogmas

Se siguen los fundamentos de DDD y SOLID **sin ser hiperestrictos**. Si una regla complica más de lo que aporta en un proyecto de este tamaño, se simplifica y se explica el motivo.

```
app/
  domain/        Entidades y reglas de negocio (Message). Sin FastAPI ni BD.
  repositories/  Interfaz del repositorio + implementaciones (InMemory, luego BD real).
  services/      Casos de uso: orquestan dominio, repositorio e integraciones.
  api/           Rutas HTTP: validan la entrada (Pydantic), llaman al servicio y traducen a HTTP.
  integrations/  Adaptadores externos (WhatsApp, IA).
  dependencies.py  Composition root: único sitio donde se elige qué implementación concreta se usa.
  main.py        Crea la app y registra los routers.
```

Principios clave:

- **El dominio no conoce la infraestructura.** `Message` no sabe nada de HTTP ni de bases de datos.
- **La lógica de negocio va en el dominio o en el servicio**, nunca en las rutas ni en los repositorios.
- **Los servicios dependen de interfaces** (`MessageRepository`), no de implementaciones concretas.
- **Los esquemas HTTP (`*Request` / `*Response`) son distintos de las entidades del dominio.**
- **Los conceptos HTTP (códigos 404, etc.) se quedan en `api/`.**

## Stack

- Python 3.12, FastAPI, Pydantic, Uvicorn, pytest.
- Entorno virtual en `.venv/`. Arrancar con: `.venv/bin/uvicorn app.main:app --reload`
- Docs interactivas en `http://localhost:8000/docs`.
