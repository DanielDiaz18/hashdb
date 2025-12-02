# 🔗 Mini-Blockchain: Base de Datos Encadenada con Hash

## Proyecto Final IH063 – Criptografía

Una aplicación educativa que simula una blockchain básica, demostrando los conceptos fundamentales de encadenamiento de registros mediante funciones hash criptográficas.

---

## 📋 Descripción

Este proyecto implementa una base de datos simplificada donde cada registro (bloque) está enlazado al anterior mediante hashes criptográficos SHA-256. Si se modifica cualquier registro histórico, la cadena se rompe y la aplicación lo detecta automáticamente.

**Nota importante:** Esto NO es una blockchain completa (no incluye minería, consenso distribuido, ni red P2P), sino una demostración educativa de los conceptos fundamentales.

---

## 🎯 Características Principales

✅ **Encadenamiento de registros** mediante hash SHA-256  
✅ **Detección automática** de alteraciones en la cadena  
✅ **Persistencia de datos** en formato JSON  
✅ **Interfaz de línea de comandos** intuitiva  
✅ **Simulación de ataques** para demostrar la seguridad  
✅ **Verificación de integridad** de toda la cadena  

---

## 🔧 Requisitos

- **Python 3.7 o superior**
- No requiere librerías externas (solo módulos estándar de Python)

---

### Ejecutar la aplicación

```bash
python3 main.py
```

---
