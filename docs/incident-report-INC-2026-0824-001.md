# REPORTE EJECUTIVO DE INCIDENTE DE SEGURIDAD

**Clasificacion:** CONFIDENCIAL - USO INTERNO

**Tipo de incidente:** Ransomware

**ID de incidente:** INC-2026-0824-001

**Fecha de deteccion:** 24 de agosto de 2026 - 00:57 UTC

**Analista responsable:** Brian Fernandez

**Marco de referencia:** NIST SP 800-61 Rev. 2 (Computer Security Incident Handling Guide)

**Estado:** CERRADO - Recuperacion completa

---

## 1. Resumen Ejecutivo

El 24 de agosto de 2026, el sistema de monitoreo Wazuh SIEM detecto actividad consistente
con un ataque de ransomware en el endpoint DESKTOP-60HVTTB (agente Vuln-SOC, IP 192.168.64.135).
El incidente fue contenido, analizado y resuelto en su totalidad dentro del entorno de
laboratorio controlado. No se vio afectada ninguna infraestructura de produccion.

La cadena de ataque siguio el patron tipico de ransomware moderno: destruccion de mecanismos
de recuperacion del sistema operativo, cifrado masivo de archivos con algoritmo AES-256 y
despliegue de notas de rescate. El total de archivos cifrados fue de 6 archivos en 3 carpetas.
La recuperacion total se logro mediante el script de descifrado con la clave retenida.

---

## 2. Framework de Respuesta — NIST SP 800-61

Este incidente fue gestionado siguiendo las cuatro fases del marco NIST SP 800-61 Rev. 2:

```
┌─────────────────────────────────────────────────────────────────────┐
│           NIST SP 800-61 - CICLO DE VIDA DEL INCIDENTE              │
│                                                                     │
│  ┌─────────────┐   ┌──────────────────┐   ┌──────────────────────┐ │
│  │  FASE 1     │   │     FASE 2       │   │       FASE 3         │ │
│  │             │   │                  │   │                      │ │
│  │ Preparacion │──▶│ Deteccion y      │──▶│ Contencion,          │ │
│  │             │   │ Analisis         │   │ Erradicacion y       │ │
│  │             │   │                  │   │ Recuperacion         │ │
│  └─────────────┘   └──────────────────┘   └──────────────────────┘ │
│         │                                           │               │
│         │          ┌──────────────────┐             │               │
│         └──────────│     FASE 4       │◀────────────┘               │
│                    │                  │                             │
│                    │ Actividad Post-  │                             │
│                    │ Incidente        │                             │
│                    └──────────────────┘                             │
└─────────────────────────────────────────────────────────────────────┘
```

### Fase 1 — Preparacion

Actividades de preparacion existentes antes del incidente:

| Elemento | Estado |
|---|---|
| SIEM (Wazuh) configurado y operativo | Activo |
| Agente Wazuh en endpoint | Activo |
| Sysmon con config personalizada | Activo |
| Reglas custom de deteccion (100020-100110) | Activas |
| Backups offline documentados | Pendiente (gap identificado) |
| Runbook de respuesta a ransomware | Este documento |
| Canal System en agente Wazuh | Faltante (gap identificado) |

### Fase 2 — Deteccion y Analisis

- **Vector de deteccion:** Wazuh SIEM — reglas custom 100200 y 100210
- **Tiempo hasta primera alerta:** Simultaneo al inicio del cifrado (< 1 segundo)
- **Tecnicas identificadas:** T1489, T1490-1, T1490-3, T1486
- **Herramientas de analisis:** Wazuh Dashboard (Discover), Sysmon EID 1/11/23
- **Indicadores previos al cifrado detectados:** T1489 (22:13) y T1490 (22:58, 23:05) el dia anterior — gap de correlacion temporal (no se genero alerta combinada pre-ransomware)

### Fase 3 — Contencion, Erradicacion y Recuperacion

| Sub-fase | Accion ejecutada | Tiempo |
|---|---|---|
| Contencion | Aislamiento del endpoint de la red | T+5 min |
| Contencion | Snapshot forense preservado | T+8 min |
| Erradicacion | Proceso cifrador terminado | T+12 min |
| Erradicacion | Script de ataque documentado y removido | T+20 min |
| Recuperacion | Ejecucion de ransomware_decrypt.py | T+2h 13min |
| Recuperacion | 6 archivos restaurados, 4 notas eliminadas | T+2h 14min |
| Verificacion | Integridad de archivos confirmada | T+2h 20min |

### Fase 4 — Actividad Post-Incidente

- Reporte ejecutivo generado (este documento)
- Gaps de deteccion identificados y documentados
- Reglas de mejora propuestas
- Lecciones aprendidas incorporadas al runbook
- Simulacro de respuesta a programar (ver BCM)

---

## 3. Linea de Tiempo del Incidente

| Timestamp (UTC) | Fase NIST | Evento |
|---|---|---|
| 23/08 22:13:38 | Deteccion | T1489 - sc.exe stop spooler detectado (Rules 92032/92052) |
| 23/08 22:58:48 | Deteccion | T1490 - vssadmin delete shadows detectado |
| 23/08 23:05:09 | Deteccion | T1490 - wbadmin delete catalog detectado |
| 24/08 00:57:31 | Deteccion | T1486 - Inicio del cifrado (python.exe -> .locked) |
| 24/08 00:57:31 | Deteccion | Primera alerta T1486 - Rule 100200 (EID 11) |
| 24/08 00:57:32 | Deteccion | 13 alertas generadas (6 x EID 11 + 7 x EID 23) |
| 24/08 01:02:00 | Contencion | Endpoint aislado de la red |
| 24/08 01:05:00 | Contencion | Snapshot forense preservado |
| 24/08 01:17:00 | Erradicacion | Proceso cifrador terminado y documentado |
| 24/08 03:10:00 | Recuperacion | Ejecucion de ransomware_decrypt.py |
| 24/08 03:11:00 | Recuperacion | 6 archivos restaurados, notas eliminadas |
| 24/08 03:30:00 | Post-Incidente | Redaccion del reporte ejecutivo |

---

## 4. Indicadores de Compromiso (IoCs)

| Tipo | Valor | Tecnica |
|---|---|---|
| Proceso | python.exe (C:\Program Files\Python312\) | T1486 |
| Extension | .locked | T1486 |
| Archivo dropeado | README_RECOVER.txt | T1486 |
| Archivo | decrypt_key.key | T1486 |
| Comando | vssadmin.exe delete shadows /all /quiet | T1490 |
| Comando | wbadmin delete catalog -quiet | T1490 |
| Comando | sc.exe stop spooler | T1489 |
| Hash MD5 | B58073DB8892B67A672906C9358020EC (vssadmin.exe) | T1490 |
| Hash SHA256 | 8C1FABCC2196E4D096B7D155837C5F699AD7F55EDBF84571E4F8E03500B7A8B0 | T1490 |
| Hash MD5 | 151FEEFF52D82BFB150B80F852DC7B50 (wbadmin.exe) | T1490 |
| Hash SHA256 | 94235BD6D75B2B11243F47D7EA2B5958433CCDE58368C2C9F1B14226E68867F6 | T1490 |

---

## 5. Impacto

| Categoria | Detalle |
|---|---|
| Archivos cifrados | 6 (.txt -> .txt.locked) |
| Carpetas afectadas | 3 (Finanzas, RRHH, Proyectos) |
| Shadow copies | Eliminadas (T1490-1) |
| Catalogo de backup | Eliminado (T1490-3) |
| Servicios detenidos | Print Spooler (T1489-1) |
| Sistemas afectados | 1 endpoint (DESKTOP-60HVTTB) |
| Datos exfiltrados | No detectado |
| Tiempo de cifrado | menos de 1 segundo (6 archivos) |
| Tiempo de recuperacion total | 2 horas 14 minutos |
| Perdida de datos | 0 (recuperacion completa via clave) |

---

## 6. Acciones de Respuesta Tomadas

1. Identificacion - Alertas detectadas en Wazuh Dashboard (rule.id: 100200 OR 100210)
2. Analisis forense - Revision de telemetria Sysmon (EID 1, 11, 23) para reconstruir cadena
3. Contencion - Endpoint aislado del entorno de red
4. Erradicacion - Proceso cifrador identificado y terminado; scripts documentados
5. Recuperacion - Ejecucion de ransomware_decrypt.py con clave decrypt_key.key
   Resultado: 6 archivos restaurados, 4 notas de rescate eliminadas
6. Verificacion - Integridad de archivos confirmada visualmente y por comparacion de contenido
7. Documentacion - Reporte ejecutivo y actualizacion de reglas de deteccion

---

## 7. Plan de Continuidad del Negocio (BCM)

### 7.1 Objetivos de Recuperacion

| Metrica | Definicion | Valor para este incidente |
|---|---|---|
| **RTO** (Recovery Time Objective) | Tiempo maximo tolerable para restaurar operaciones | 4 horas |
| **RPO** (Recovery Point Objective) | Maximo periodo de perdida de datos aceptable | 24 horas (ultimo backup) |
| **MTTR** (Mean Time to Recover) | Tiempo real de recuperacion en este incidente | 2 horas 14 minutos |
| **RTO cumplido** | El MTTR fue menor al RTO definido | SI (2h 14min < 4h) |

### 7.2 Analisis de Impacto al Negocio (BIA)

| Area/Sistema | Criticidad | Estado durante incidente | Impacto |
|---|---|---|---|
| Documentos Finanzas | Alta | Cifrado (carpeta señuelo) | Bajo (datos de prueba) |
| Documentos RRHH | Alta | Cifrado (carpeta señuelo) | Bajo (datos de prueba) |
| Documentos Proyectos | Media | Cifrado (carpeta señuelo) | Bajo (datos de prueba) |
| Wazuh SIEM | Critica | Operativo durante todo el incidente | Sin impacto |
| Agente de monitoreo | Critica | Activo en el endpoint comprometido | Sin impacto |
| Backups offline | Alta | No configurados en este entorno | Gap critico identificado |

> En un entorno de produccion real, los documentos de Finanzas y RRHH serian clasificados
> como CRITICOS con un RTO de 1 hora y un RPO de 4 horas, requiriendo backups incrementales
> cada 4 horas y backups completos diarios en storage offline.

### 7.3 Estrategia de Continuidad Durante el Incidente

#### Mientras el sistema esta aislado (fase de contencion/erradicacion):

| Proceso afectado | Procedimiento alternativo | Responsable |
|---|---|---|
| Acceso a documentos Finanzas | Uso de copias en backup offline o storage en la nube alternativo | Area de Finanzas |
| Acceso a documentos RRHH | Uso de backup previo o sistema de contingencia | Area de RRHH |
| Operaciones del endpoint afectado | Reasignacion temporal a otro equipo | IT / Supervisor |
| Comunicacion interna | Canal alternativo (Slack/Teams fuera del dominio afectado) | TI |
| Reporte a stakeholders | Notificacion inicial dentro de los 30 minutos de confirmado el incidente | CISO / Gerencia |

#### Comunicacion ante un incidente de ransomware:

```
T+0  → Deteccion automatica (Wazuh SIEM)
T+5  → Analista SOC confirma y escala al equipo de respuesta
T+15 → Notificacion al CISO / responsable de seguridad
T+30 → Comunicacion inicial a gerencia (sin revelar detalles tecnicos publicamente)
T+60 → Evaluacion del alcance y decision: pago/no-pago (nunca recomendado), recovery
T+2h → Actualizacion de estado a stakeholders
T+Xh → Declaracion de incidente cerrado tras recuperacion verificada
```

### 7.4 Plan de Prueba del BCM

| Actividad | Frecuencia | Responsable |
|---|---|---|
| Simulacro de ransomware (tabletop exercise) | Anual | CISO + Equipo SOC |
| Prueba de restore desde backup offline | Trimestral | IT / SysAdmin |
| Revision del runbook de respuesta | Semestral | Analista SOC Senior |
| Actualizacion de reglas de deteccion | Post-incidente + Trimestral | Analista SOC |
| Verificacion de RTO/RPO | Semestral | CISO + Area de Negocio |

### 7.5 Lecciones Aprendidas — BCM

1. **Backup offline ausente:** La eliminacion exitosa de shadow copies (T1490) deja al sistema
   sin mecanismo de recuperacion nativo. Un backup offline (air-gapped) es el control
   preventivo mas critico para ransomware y debe implementarse antes de cualquier otro control.

2. **RTO/RPO no formalizados previo al incidente:** Los objetivos de recuperacion deben
   definirse por anticipado en funcion de la criticidad del negocio, no durante el incidente.

3. **Sin correlacion temporal T1489+T1490 → pre-alerta:** Las tecnicas de preparacion del
   atacante (detencion de servicios + borrado de backups) ocurrieron 2 horas antes del cifrado
   sin generar una alerta combinada. Una regla de correlacion habria permitido contener antes
   del impacto real.

---

## 8. Recomendaciones

| Prioridad | Categoria | Recomendacion |
|---|---|---|
| Critica | BCM | Implementar backup offline (air-gapped) con RPO de 4 horas |
| Alta | Deteccion | Reglas custom para T1489/T1490 con mapeo correcto a las tecnicas |
| Alta | Visibilidad | Canal System en agente Wazuh para capturar EID 7036 |
| Alta | Correlacion | Regla temporal: T1489 + T1490 en ventana de 30 min = pre-alerta nivel 14 |
| Media | Monitoreo | Agregar python.exe al monitoreo de EID 1 en Sysmon |
| Media | BCM | Formalizar RTO/RPO por sistema antes del proximo ejercicio |
| Media | BCM | Programar simulacro tabletop anual de ransomware |
| Baja | Hardening | Revisar politica de ejecucion de scripts Python en endpoints |
| Baja | Proceso | Definir arbol de comunicacion y plantilla de notificacion a stakeholders |

---

## 9. Hallazgos Tecnicos

### Gap 1 — EID 7036 no recolectado por Wazuh
El canal System no esta en ossec.conf. La confirmacion del efecto de T1489 no llego al SIEM.
**Fix:** Agregar localfile System a ossec.conf del agente.

### Gap 2 — Deteccion generica para T1489/T1490
Dispararon reglas T1059.003 (Command Shell), no T1489/T1490. El SIEM no identifico la
preparacion de ransomware como tal.
**Fix:** Reglas custom para vssadmin/wbadmin/sc.exe con argumentos destructivos.

### Gap 3 — EID 23 deshabilitado en config base de Sysmon
FileDelete completamente comentado en la config de SwiftOnSecurity. Requirio modificacion manual.
**Leccion:** Revisar activamente la config de Sysmon para casos de uso especificos.

### Gap 4 — Sin correlacion pre-ataque
T1489 y T1490 ocurrieron 2+ horas antes del cifrado. Sin regla de correlacion temporal,
el SOC no recibio alerta anticipada de preparacion de ransomware.
**Fix:** Regla de correlacion: si T1489 + T1490 en menos de 60 minutos → alerta nivel 14.

### Gap 5 — python.exe fuera del scope de monitoreo
El cifrador no disparo EID 1 porque python.exe no estaba en el include de Sysmon.
**Fix:** Agregar python.exe al ProcessCreate include del sysmonconfig.

---

## 10. Firmas y Aprobacion

| Rol | Nombre | Fecha |
|---|---|---|
| Analista SOC (Autor) | Brian Fernandez | 24/08/2026 |
| Revisor de Seguridad | | |
| CISO / Aprobador | | |

---

**Clasificacion del documento:** CONFIDENCIAL - USO INTERNO
**Proxima revision:** 90 dias post-cierre o ante nuevo incidente similar
**Marco de referencia:** NIST SP 800-61 Rev. 2 | ISO/IEC 27035 | SANS PICERL
