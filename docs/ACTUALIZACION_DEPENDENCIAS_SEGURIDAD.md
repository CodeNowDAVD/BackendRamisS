# Actualización de dependencias por hallazgos de seguridad (Snyk)

Este documento resume los **cambios en dependencias y código** realizados para atender avisos de **Snyk** y CVEs relacionados. Sirve para que quien revise el backend sepa **qué se tocó**, **por qué** y **qué probar**.

---

## Migración mayor (2026-04-23): FastAPI, Starlette, Pydantic v2, JWT

### Objetivo

Cerrar los hallazgos **“gordos”** que Snyk reportaba sobre:

- **FastAPI** antiguo (p. ej. ReDoS en parsing de `Content-Type` con multipart, **CVE-2024-24762**).
- **Starlette** antigua (límites en multipart, `UploadFile`, **ReDoS** en cabecera `Range` / `FileResponse`, etc.).
- **`ecdsa`** transitivo vía **`python-jose`** (sin parche satisfactorio en el ecosistema puro-Python).

### Dependencias (`requirements.txt`)

| Paquete | Antes (referencia) | Después |
|---------|-------------------|---------|
| `fastapi` | 0.95.2 | **0.128.8** |
| `uvicorn[standard]` | 0.22.0 | **0.34.0** |
| `pydantic` | 1.10.13 | **2.11.4** |
| JWT | `python-jose[cryptography]` | **`PyJWT[crypto]==2.12.0`** (CVE-2024-32597 / cabecera `crit` en JWS) |
| `pyasn1` | (solo transitiva) | **>= 0.6.3** (pin explícito para CVEs de `pyasn1`) |

**Sin cambio de versión en esta migración:** `SQLAlchemy`, `psycopg2-binary`, `python-dotenv`, `argon2-cffi`, `python-multipart`, `pandas`, `openpyxl`, `Pillow`, `xlrd`, `pdfplumber`, `passlib`, `email-validator` (ya estaban actualizados en pasos previos).

**Transitivas relevantes:** `starlette` pasa a la línea compatible con FastAPI 0.128.x (≥ 0.40, típicamente reciente respecto a 0.27.x).

### Cambios de código (resumen para revisores)

| Área | Cambio |
|------|--------|
| **Pydantic v2** | `class Config` / `orm_mode` → `model_config = ConfigDict(from_attributes=True)` donde aplicaba. |
| **Validadores** | `app/schemas/orden_compra_schema.py`: `@validator` → `@field_validator` / `@model_validator` (el archivo tenía validadores huérfanos; se reordenó y corrigió la lógica). |
| **Routers** | `rq.dict()` → `rq.model_dump()` en `rqs_router` y `rq_item_router`. |
| **JWT** | `app/security/jwt_handler.py` y `jwt_manager.py` usan **PyJWT**; `exp` con **tiempo UTC** (`datetime.now(timezone.utc)`). |
| **Auth** | `app/dependencies/auth_dependencies.py`: captura **`jwt.PyJWTError`** en lugar de `Exception` genérico. |
| **Ciclo de vida** | `app/main.py`: `@app.on_event("startup")` sustituido por **`lifespan`** (recomendado en FastAPI reciente). |
| **Esquemas RQ** | `app/schemas/rq_schema.py`: eliminada **clase duplicada** `RQItemPendienteResponse` (solo vivía la segunda definición). Import unificado desde `rq_item_schema` en `rqs_router`. |
| **Almacén préstamo** | `app/schemas/almacen_prestamo.py`: **`TipoArticuloSchema`** pasaba a heredar de `sqlalchemy.Enum` por error; corregido a **`enum.Enum`**. |

### Verificación obligatoria tras fusionar

- [ ] `python3.11 -m pip install -r requirements.txt` (alineado con `runtime.txt`).
- [ ] `uvicorn app.main:app --reload` y smoke test `/`.
- [ ] **Login** y llamadas con **Bearer token**.
- [ ] **Multipart** (subidas) y flujos **PDF / Excel / firmas**.
- [ ] `pytest` (tests bajo `app/test/`).
- [ ] **Nuevo escaneo Snyk** sobre la rama.

---

## Historial de actualizaciones puntuales (antes de la migración mayor)

| Paquete | Evolución | Motivo principal |
|---------|-----------|------------------|
| `Pillow` | 10.2 → 12.2.0 | CVEs (búfer, PSD, FITS/GZIP, etc.). |
| `python-dotenv` | 1.0.1 → 1.2.2 | CVE-2024-28684 (symlinks). |
| `python-multipart` | 0.0.9 → 0.0.26 | Varios CVEs de parsing / DoS. |
| `pdfplumber` | 0.10.3 → 0.11.9 | `pdfminer.six` parcheado. |

---

## Historial del documento

| Fecha | Cambio |
|-------|--------|
| 2026-04-22 | Creación: registro de bumps iniciales en `requirements.txt`. |
| 2026-04-23 | Migración FastAPI 0.128 + Pydantic v2 + PyJWT; actualización de esquemas, `main`, auth y documentación. |
