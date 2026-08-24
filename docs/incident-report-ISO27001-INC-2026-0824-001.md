# REPORTE DE INCIDENTE DE SEGURIDAD DE LA INFORMACION
## Alineado a ISO/IEC 27001:2022

**Clasificacion:** CONFIDENCIAL - USO INTERNO

**Tipo de incidente:** Ransomware / Cifrado de datos

**ID de incidente:** INC-2026-0824-001

**Fecha de deteccion:** 24 de agosto de 2026 - 00:57 UTC

**Analista responsable:** Braian Fernandez

**Marco de gestión:   ISO/IEC 27001:2022

**Marco operativo:    NIST SP 800-61 Rev. 2

**Matriz de amenazas: MITRE ATT&CK v14

**Estado:** CERRADO - Recuperacion completa y verificada

---

## 1. Resumen Ejecutivo

El 24 de agosto de 2026, el sistema de monitoreo Wazuh SIEM detecto un incidente de
ransomware en el endpoint DESKTOP-60HVTTB (agente Vuln-SOC, IP 192.168.64.135).
El incidente fue identificado, contenido, erradicado y recuperado en su totalidad dentro
del entorno de laboratorio controlado. No se vio comprometida infraestructura de produccion.

La cadena de ataque comprende las tecnicas MITRE ATT&CK T1489, T1490 y T1486, siguiendo
el patron clasico de ransomware moderno: destruccion de mecanismos de recuperacion, cifrado
de datos con AES-256 y extorsion via nota de rescate. La recuperacion total fue posible
gracias a la disponibilidad de la clave de descifrado retenida en el entorno controlado.

Este reporte esta alineado a los controles de ISO/IEC 27001:2022, Anexo A, y sirve como
evidencia de cumplimiento del proceso de gestion de incidentes de seguridad de la informacion.

---

## 2. Mapeo ISO/IEC 27001:2022 — Controles Aplicables

### Controles del Anexo A activados por este incidente

| Control ISO 27001:2022 | Descripcion | Estado en este incidente |
|---|---|---|
| **A.5.24** | Planificacion y preparacion de la gestion de incidentes | Parcial — runbook existente, sin simulacros previos |
| **A.5.25** | Evaluacion y decision sobre eventos de seguridad | Cumplido — alertas triadas y escaladas correctamente |
| **A.5.26** | Respuesta a incidentes de seguridad de la informacion | Cumplido — contencion, erradicacion y recuperacion ejecutadas |
| **A.5.27** | Aprendizaje de los incidentes de seguridad | Cumplido — gaps documentados y mejoras propuestas |
| **A.5.28** | Recoleccion de evidencia | Cumplido — telemetria Sysmon + alertas Wazuh preservadas |
| **A.5.29** | Seguridad de la informacion durante la interrupcion | Parcial — sin procedimientos formales de continuidad previos |
| **A.5.30** | Preparacion de TIC para la continuidad del negocio | No cumplido — backups offline no configurados (gap critico) |
| **A.6.8** | Notificacion de eventos de seguridad | Parcial — deteccion automatica, sin arbol de notificacion formal |
| **A.8.7** | Proteccion contra malware | Parcial — Defender activo pero sin politica de scripting Python |
| **A.8.8** | Gestion de vulnerabilidades tecnicas | Pendiente — revision de politica de ejecucion de scripts |
| **A.8.13** | Copia de seguridad de la informacion | No cumplido — shadow copies eliminadas, sin backup offline |
| **A.8.16** | Actividades de monitoreo | Cumplido — Sysmon + Wazuh activos con reglas custom |
| **A.8.24** | Uso de criptografia | Gestionado — cifrado AES-256 identificado y revertido |

---

## 3. Gestion del Incidente — PDCA (ISO 27001)

ISO/IEC 27001 utiliza el ciclo PDCA (Plan-Do-Check-Act) como base del SGSI.
La respuesta a este incidente se refleja en ese ciclo:

```
┌──────────────────────────────────────────────────────────────────┐
│                  CICLO PDCA — ISO 27001                          │
│                                                                  │
│   PLAN                         DO                               │
│   ────────────────────         ──────────────────────           │
│   • Runbook de respuesta   --> • Contencion del endpoint        │
│   • Reglas de deteccion    --> • Eradicacion del proceso        │
│   • Wazuh + Sysmon         --> • Recuperacion con decrypt       │
│   • RTO/RPO definidos      --> • Comunicacion a stakeholders    │
│          │                              │                        │
│          ▼                              ▼                        │
│   ACT                          CHECK                            │
│   ────────────────────         ──────────────────────           │
│   • Nuevas reglas custom   <-- • Revision de alertas Wazuh     │
│   • Config Sysmon EID 23   <-- • Gaps de cobertura analizados  │
│   • Backup offline         <-- • RTO vs MTTR comparados        │
│   • Correlacion T1490+T1489<-- • Post-mortem del incidente     │
└──────────────────────────────────────────────────────────────────┘
```

---

## 4. Framework de Respuesta — NIST SP 800-61 (Complementario)

### Fase 1 — Preparacion (ISO A.5.24)

| Elemento | Estado | Control ISO |
|---|---|---|
| SIEM (Wazuh) configurado | Activo | A.8.16 |
| Agente Wazuh en endpoint | Activo | A.8.16 |
| Sysmon con config personalizada | Activo | A.8.16 |
| Reglas custom de deteccion (100020-100210) | Activas | A.5.25 |
| Backups offline | No configurado | A.8.13 — GAP CRITICO |
| Runbook de respuesta | Existente (este doc) | A.5.24 |
| Politica de ejecucion de scripts | No definida | A.8.7 |
| Arbol de notificacion formal | No definido | A.6.8 |

### Fase 2 — Deteccion y Analisis (ISO A.5.25 / A.8.16)

- **Vector de deteccion:** Wazuh SIEM — reglas custom 100200 y 100210
- **Tiempo hasta primera alerta:** Simultaneo al inicio del cifrado (< 1 segundo)
- **Tecnicas identificadas:** T1489, T1490-1, T1490-3, T1486
- **Herramientas de analisis:** Wazuh Dashboard, Sysmon EID 1/11/23
- **Evidencia preservada:** Telemetria completa en indice wazuh-alerts-4.x-2026.08.23/24

### Fase 3 — Contencion, Erradicacion y Recuperacion (ISO A.5.26 / A.5.29)

| Sub-fase | Accion | Control ISO | Tiempo |
|---|---|---|---|
| Contencion | Aislamiento de red del endpoint | A.5.26 | T+5 min |
| Contencion | Snapshot forense preservado | A.5.28 | T+8 min |
| Erradicacion | Proceso cifrador terminado | A.5.26 | T+12 min |
| Erradicacion | Script documentado y removido | A.5.26 | T+20 min |
| Recuperacion | Ejecucion de ransomware_decrypt.py | A.5.26 | T+2h 13min |
| Recuperacion | 6 archivos restaurados | A.5.29 | T+2h 14min |
| Verificacion | Integridad confirmada | A.5.26 | T+2h 20min |

### Fase 4 — Actividad Post-Incidente (ISO A.5.27)

- Reporte ejecutivo generado (este documento)
- Gaps identificados y documentados con controles ISO asociados
- Mejoras de deteccion implementadas (EID 11/23 en Sysmon, reglas 100200/100210)
- Lecciones aprendidas incorporadas al SGSI
- Plan de mejora continua propuesto (ver seccion 9)

---

## 5. Linea de Tiempo del Incidente

| Timestamp (UTC) | Fase NIST / ISO | Evento |
|---|---|---|
| 23/08 22:13:38 | Deteccion / A.5.25 | T1489 - sc.exe stop spooler (Rules 92032/92052) |
| 23/08 22:58:48 | Deteccion / A.5.25 | T1490 - vssadmin delete shadows detectado |
| 23/08 23:05:09 | Deteccion / A.5.25 | T1490 - wbadmin delete catalog detectado |
| 24/08 00:57:31 | Deteccion / A.5.25 | T1486 - Inicio del cifrado (python.exe) |
| 24/08 00:57:31 | Deteccion / A.8.16 | Primera alerta T1486 - Rule 100200 (EID 11) |
| 24/08 00:57:32 | Deteccion / A.8.16 | 13 alertas generadas (6xEID11 + 7xEID23) |
| 24/08 01:02:00 | Contencion / A.5.26 | Endpoint aislado de la red |
| 24/08 01:05:00 | Contencion / A.5.28 | Snapshot forense preservado |
| 24/08 01:17:00 | Erradicacion / A.5.26 | Proceso cifrador terminado |
| 24/08 03:10:00 | Recuperacion / A.5.29 | Ejecucion de ransomware_decrypt.py |
| 24/08 03:11:00 | Recuperacion / A.5.29 | 6 archivos restaurados, notas eliminadas |
| 24/08 03:30:00 | Post-Incidente / A.5.27 | Redaccion del reporte ejecutivo |

---

## 6. Indicadores de Compromiso (IoCs)

| Tipo | Valor | Tecnica MITRE | Control ISO |
|---|---|---|---|
| Proceso | python.exe (C:\Program Files\Python312\) | T1486 | A.8.7 |
| Extension | .locked | T1486 | A.8.7 |
| Archivo dropeado | README_RECOVER.txt | T1486 | A.5.25 |
| Archivo | decrypt_key.key | T1486 | A.8.24 |
| Comando | vssadmin.exe delete shadows /all /quiet | T1490 | A.8.13 |
| Comando | wbadmin delete catalog -quiet | T1490 | A.8.13 |
| Comando | sc.exe stop spooler | T1489 | A.5.26 |
| Hash MD5 | B58073DB8892B67A672906C9358020EC (vssadmin.exe) | T1490 | A.5.28 |
| Hash SHA256 | 8C1FABCC2196E4D096B7D155837C5F699AD7F55EDBF84571E4F8E03500B7A8B0 | T1490 | A.5.28 |
| Hash MD5 | 151FEEFF52D82BFB150B80F852DC7B50 (wbadmin.exe) | T1490 | A.5.28 |
| Hash SHA256 | 94235BD6D75B2B11243F47D7EA2B5958433CCDE58368C2C9F1B14226E68867F6 | T1490 | A.5.28 |

---

## 7. Impacto

| Categoria | Detalle | Control ISO afectado |
|---|---|---|
| Archivos cifrados | 6 (.txt -> .txt.locked) | A.8.13 |
| Carpetas afectadas | 3 (Finanzas, RRHH, Proyectos) | A.8.13 |
| Shadow copies | Eliminadas (T1490-1) | A.8.13 |
| Catalogo de backup | Eliminado (T1490-3) | A.8.13 |
| Servicios detenidos | Print Spooler (T1489-1) | A.5.29 |
| Sistemas afectados | 1 endpoint (DESKTOP-60HVTTB) | A.5.26 |
| Datos exfiltrados | No detectado | A.5.28 |
| Tiempo de recuperacion | 2 horas 14 minutos | A.5.30 |
| Perdida de datos | 0 (recuperacion completa) | A.8.13 |

---

## 8. Plan de Continuidad del Negocio (BCM) — ISO A.5.29 / A.5.30

### 8.1 Objetivos de Recuperacion

| Metrica | Definicion | Valor objetivo | Valor real (este incidente) |
|---|---|---|---|
| **RTO** | Tiempo maximo para restaurar operaciones | 4 horas | 2h 14min (cumplido) |
| **RPO** | Maximo periodo de perdida de datos aceptable | 24 horas | 0 (clave disponible) |
| **MTTR** | Tiempo real de recuperacion | <= RTO | 2h 14min |

### 8.2 Analisis de Impacto al Negocio (BIA) — ISO A.5.29

| Area / Sistema | Clasificacion ISO | Criticidad | Estado durante incidente | Control aplicado |
|---|---|---|---|---|
| Documentos Finanzas | Confidencial | Alta | Cifrado (señuelo) | A.8.13 |
| Documentos RRHH | Confidencial | Alta | Cifrado (señuelo) | A.8.13 |
| Documentos Proyectos | Interno | Media | Cifrado (señuelo) | A.8.13 |
| Wazuh SIEM | Critico | Maxima | Operativo | A.8.16 |
| Agente de monitoreo | Critico | Maxima | Activo | A.8.16 |
| Backups offline | Critico | Maxima | No configurados | A.8.13 — GAP |

### 8.3 Estrategia de Continuidad — ISO A.5.29 / A.5.30

#### Durante el aislamiento del endpoint:

| Proceso afectado | Procedimiento alternativo | Responsable | Control ISO |
|---|---|---|---|
| Acceso a documentos Finanzas | Backup offline o cloud alternativo | Area Finanzas | A.5.29 |
| Acceso a documentos RRHH | Sistema de contingencia | Area RRHH | A.5.29 |
| Operaciones del endpoint | Reasignacion temporal | IT | A.5.29 |
| Comunicacion interna | Canal alternativo fuera del dominio | TI | A.5.29 |
| Notificacion stakeholders | Dentro de los 30 min de confirmacion | CISO | A.6.8 |

#### Arbol de comunicacion (ISO A.6.8):

```
T+0  --> Deteccion automatica (Wazuh SIEM)
T+5  --> Analista SOC confirma y escala al equipo de respuesta
T+15 --> Notificacion al CISO / Responsable de Seguridad
T+30 --> Comunicacion inicial a Gerencia (ISO A.6.8)
T+60 --> Evaluacion de alcance y decision de recuperacion
T+2h --> Actualizacion de estado a stakeholders
T+Xh --> Declaracion de incidente cerrado (ISO A.5.27)
```

### 8.4 Plan de Prueba del BCM — ISO A.5.30

| Actividad | Frecuencia | Responsable | Control ISO |
|---|---|---|---|
| Simulacro de ransomware (tabletop exercise) | Anual | CISO + SOC | A.5.24 |
| Prueba de restore desde backup offline | Trimestral | IT / SysAdmin | A.8.13 |
| Revision del runbook de respuesta | Semestral | Analista SOC Senior | A.5.24 |
| Actualizacion de reglas de deteccion | Post-incidente + Trimestral | Analista SOC | A.8.16 |
| Verificacion de RTO/RPO vs operaciones reales | Semestral | CISO + Negocio | A.5.30 |
| Auditoria interna de controles ISO 27001 | Anual | Auditor interno | ISO 9.2 |

---

## 9. Hallazgos, Gaps y Plan de Mejora Continua — ISO A.10.2

### Gap 1 — EID 7036 no recolectado (A.8.16)
**Descripcion:** Canal System no configurado en ossec.conf. El estado real del servicio
detenido (T1489) no llego al SIEM.
**Control afectado:** A.8.16 Actividades de monitoreo
**Accion correctiva:** Agregar canal System al agente Wazuh
**Prioridad:** Alta | **Responsable:** Analista SOC | **Plazo:** 7 dias

### Gap 2 — Deteccion generica para T1489/T1490 (A.5.25)
**Descripcion:** Las tres tecnicas dispararon T1059.003 en vez de T1489/T1490.
El SIEM no identifico la preparacion de ransomware.
**Control afectado:** A.5.25 Evaluacion de eventos de seguridad
**Accion correctiva:** Reglas custom para vssadmin/wbadmin/sc.exe con args destructivos
**Prioridad:** Alta | **Responsable:** Analista SOC | **Plazo:** 14 dias

### Gap 3 — EID 23 deshabilitado en Sysmon (A.8.16)
**Descripcion:** FileDelete completamente comentado en config base SwiftOnSecurity.
Requirio intervencion manual para habilitarlo.
**Control afectado:** A.8.16 Actividades de monitoreo
**Accion correctiva:** Revisar activamente la config de Sysmon para casos de uso especificos
**Prioridad:** Media | **Responsable:** Analista SOC | **Plazo:** 14 dias

### Gap 4 — Sin correlacion pre-ataque T1489+T1490 (A.5.25)
**Descripcion:** T1489 y T1490 ocurrieron 2+ horas antes del cifrado sin generar
una alerta combinada de "preparacion de ransomware en curso".
**Control afectado:** A.5.25 Evaluacion y decision sobre eventos
**Accion correctiva:** Regla de correlacion: T1489 + T1490 < 60 min = alerta nivel 14
**Prioridad:** Alta | **Responsable:** Analista SOC | **Plazo:** 30 dias

### Gap 5 — Backup offline ausente (A.8.13)
**Descripcion:** La eliminacion exitosa de shadow copies deja al sistema sin recuperacion
nativa. La recuperacion dependio de la clave en manos del "atacante". En un escenario real
sin clave disponible, la perdida de datos seria total.
**Control afectado:** A.8.13 Copia de seguridad de la informacion
**Accion correctiva:** Implementar backup offline (air-gapped) con RPO de 4 horas
**Prioridad:** Critica | **Responsable:** IT / SysAdmin | **Plazo:** Inmediato

### Gap 6 — Sin politica de scripting Python en endpoints (A.8.7)
**Descripcion:** python.exe pudo ejecutarse sin restricciones en el endpoint.
**Control afectado:** A.8.7 Proteccion contra malware
**Accion correctiva:** Revisar politica de ejecucion de aplicaciones / Application Whitelisting
**Prioridad:** Media | **Responsable:** IT | **Plazo:** 30 dias

### Gap 7 — Sin arbol de notificacion formal (A.6.8)
**Descripcion:** No existe un procedimiento documentado de escalado y notificacion
para incidentes de seguridad.
**Control afectado:** A.6.8 Notificacion de eventos de seguridad
**Accion correctiva:** Definir arbol de comunicacion y plantilla de notificacion
**Prioridad:** Media | **Responsable:** CISO | **Plazo:** 30 dias

---

## 10. Recomendaciones — Priorizadas por Control ISO

| Prioridad | Control ISO | Recomendacion |
|---|---|---|
| Critica | A.8.13 | Backup offline (air-gapped) con RPO de 4 horas |
| Alta | A.5.25 | Reglas custom para T1489/T1490 con mapeo correcto |
| Alta | A.8.16 | Canal System en agente Wazuh (EID 7036) |
| Alta | A.5.25 | Regla de correlacion temporal T1489+T1490 pre-alerta |
| Media | A.8.16 | Agregar python.exe al monitoreo EID 1 en Sysmon |
| Media | A.5.30 | Formalizar RTO/RPO por sistema antes del proximo ejercicio |
| Media | A.5.24 | Programar simulacro tabletop anual de ransomware |
| Media | A.6.8 | Definir arbol de comunicacion y escalado formal |
| Baja | A.8.7 | Revisar politica de ejecucion de scripts en endpoints |
| Baja | A.8.8 | Revision periodica de vulnerabilidades tecnicas |

---

## 11. Declaracion de Conformidad ISO/IEC 27001:2022

Este reporte ha sido elaborado siguiendo los requisitos de las clausulas 6.1.2, 8.2, 9.1
y 10.2 de ISO/IEC 27001:2022, y los controles del Anexo A referenciados en cada seccion.

| Clausula ISO 27001 | Descripcion | Evidencia en este reporte |
|---|---|---|
| 6.1.2 | Evaluacion de riesgos de seguridad | BIA, tabla de impacto (seccion 7) |
| 8.2 | Evaluacion de riesgos de la informacion | Gaps y plan de mejora (seccion 9) |
| 9.1 | Seguimiento, medicion, analisis y evaluacion | RTO/RPO/MTTR (seccion 8.1) |
| 10.2 | Mejora continua | Plan de accion post-incidente (seccion 9) |
| Anexo A.5.24-5.30 | Gestion de incidentes de seguridad | Secciones 4, 5, 8 |
| Anexo A.6.8 | Notificacion de eventos | Arbol de comunicacion (seccion 8.3) |
| Anexo A.8.7 | Proteccion contra malware | Gaps 5 y 6 (seccion 9) |
| Anexo A.8.13 | Copia de seguridad | Gap critico 5 (seccion 9) |
| Anexo A.8.16 | Actividades de monitoreo | Deteccion Wazuh/Sysmon (secciones 4, 5) |

---

## 12. Firmas y Aprobacion

| Rol | Nombre | Fecha | Firma |
|---|---|---|---|
| Analista SOC (Autor) | Brian Fernandez | 24/08/2026 | |
| Revisor de Seguridad (ISO 27001) | | | |
| CISO / Aprobador | | | |
| Responsable del SGSI | | | |

---

**Clasificacion del documento:** CONFIDENCIAL - USO INTERNO
**Proximo ciclo de revision:** 90 dias post-cierre o ante nuevo incidente similar
**Marcos normativos:** ISO/IEC 27001:2022 | NIST SP 800-61 Rev. 2 | MITRE ATT&CK v14
**Version:** 2.0 | **Reemplaza:** incident-report-INC-2026-0824-001.md v1.0
