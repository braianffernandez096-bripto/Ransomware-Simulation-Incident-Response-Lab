# Reporte de incidente INC-2026-0824-001: ransomware simulado

**Tipo de incidente:** ransomware (T1489, T1490, T1486)
**Inicio:** 23/08/2026 22:13 UTC · **Cifrado:** 24/08/2026 00:57 UTC
**Equipo afectado:** DESKTOP-60HVTTB (agente `Vuln-SOC`, 192.168.64.135)
**Analista:** Braian Fernandez
**Estado:** cerrado
**Marcos de referencia:** ISO/IEC 27001:2022 (Anexo A), NIST SP 800-61, MITRE ATT&CK

> **Alcance:** este reporte documenta un ejercicio de laboratorio aislado. No hay una organización real detrás: los roles (CISO, áreas de Finanzas y RRHH), los objetivos de recuperación y los plazos son supuestos para practicar el formato de un reporte de incidente. Todas las acciones técnicas se ejecutaron y las capturas están en `evidence/`.

---

## 1. Resumen

Entre el 23/08 a las 22:13 y el 24/08 a las 00:57 UTC simulé en una VM con Windows 10 una cadena de ransomware: detención de un servicio (T1489), borrado de shadow copies y del catálogo de backup (T1490) y cifrado de seis archivos señuelo (T1486).

Wazuh generó alertas en cada paso, pero las dos primeras fases solo las vieron reglas genéricas de shell (92032 y 92052). El cifrado lo detectaron mis reglas 100200 y 100210 en menos de un segundo.

La respuesta del ejercicio empezó con el cifrado. En un caso real, las alertas de las 22:13 y las 22:58 eran la oportunidad de frenar el ataque antes de perder los backups.

Recuperé los archivos con la clave que el simulador dejó en el mismo equipo. Sin esa clave, la recuperación habría dependido de un backup offline, que no tenía. Ordené el reporte según los controles del Anexo A de ISO/IEC 27001:2022.

---

## 2. Controles ISO/IEC 27001:2022 que se ejercitaron

| Control | Qué se vio en el lab | Estado |
|---|---|---|
| A.5.24 Planificación y preparación de la gestión de incidentes | Hay un runbook, pero lo escribí después del incidente y no hubo simulacros previos | Parcial |
| A.5.25 Evaluación y decisión sobre eventos | Confirmé las alertas a mano, sin proceso formal de triage | Parcial |
| A.5.26 Respuesta a incidentes | Contención, erradicación y recuperación del equipo afectado | Cubierto en el lab |
| A.5.27 Aprendizaje de los incidentes | Gaps documentados con acciones correctivas (sección 9) | Cubierto en el lab |
| A.5.28 Recolección de evidencia | Telemetría de Sysmon, alertas de Wazuh y un snapshot del equipo | Cubierto en el lab |
| A.5.29 Seguridad durante una interrupción | No hay procedimientos formales de continuidad | Parcial |
| A.5.30 Preparación de las TIC para la continuidad | No hay backups offline | No cubierto |
| A.6.8 Notificación de eventos | La detección fue automática, pero no hay un árbol de notificación formal | Parcial |
| A.8.7 Protección contra malware | Defender estaba activo, pero sin política para scripts de Python | Parcial |
| A.8.13 Copia de seguridad | Shadow copies y catálogo eliminados; sin backup offline | No cubierto |
| A.8.15 Registro y A.8.16 Monitoreo | Sysmon y Wazuh activos con reglas propias, pero con gaps (EID 7036 sin recolectar, EID 23 deshabilitado) | Parcial |

---

## 3. Gestión del incidente con el ciclo PDCA

ISO 27001 suele explicarse con el ciclo PDCA (planificar, hacer, verificar, actuar). Lo uso para ordenar lo que hice en este incidente:

| Fase | Qué hice |
|---|---|
| Plan | Runbook de respuesta, reglas de detección, Wazuh + Sysmon, RTO y RPO definidos como supuestos |
| Do | Contención del endpoint, erradicación del script, recuperación con el script de descifrado |
| Check | Revisión de las alertas de Wazuh, análisis de los gaps de cobertura, comparación de RTO contra el tiempo real de recuperación |
| Act | Reglas propias nuevas, config de Sysmon (EID 23), backup offline, correlación de T1489 y T1490, post-mortem |

La comunicación a los interesados quedó definida (sección 8.3), pero no la ejercité.

---

## 4. Respuesta según NIST SP 800-61

Uso las fases de NIST SP 800-61 como complemento de ISO para ordenar la respuesta.

### Fase 1. Preparación (ISO A.5.24)

| Elemento | Estado | Control ISO |
|---|---|---|
| SIEM (Wazuh) | Activo | A.8.16 |
| Agente de Wazuh en el endpoint | Activo | A.8.16 |
| Sysmon con config personalizada | Activo | A.8.16 |
| Reglas propias de detección (100020 a 100210) | Activas | A.5.25 |
| Backups offline | No configurados (gap crítico) | A.8.13 |
| Runbook de respuesta | Este documento, escrito después del incidente | A.5.24 |
| Política de ejecución de scripts | No definida | A.8.7 |
| Árbol de notificación formal | No definido | A.6.8 |

### Fase 2. Detección y análisis (ISO A.5.25 y A.8.16)

- **Primera alerta del incidente:** 23/08 22:13:38, por T1489 (regla genérica). La primera alerta de impacto fue a las 00:57:31 (regla 100200).
- **Las dos fases previas pasaron como ejecución de shell.** Wazuh las clasificó como T1059.003 (Windows Command Shell), no como T1489 ni T1490.
- **El cifrado sí quedó bien identificado.** Las reglas 100200 y 100210 generaron 13 alertas, sin demora.
- **Técnicas identificadas:** T1489, T1490-1, T1490-3 y T1486.
- **Herramientas:** Wazuh Dashboard y telemetría de Sysmon (EID 1, 11 y 23).
- **Evidencia:** índice `wazuh-alerts-4.x-2026.08.23/24` y capturas en `evidence/`.

### Fase 3. Contención, erradicación y recuperación (ISO A.5.26 y A.5.29)

| Etapa | Acción | Control ISO | Tiempo desde el cifrado |
|---|---|---|---|
| Contención | Aislé el endpoint de la red | A.5.26 | 5 min |
| Contención | Tomé un snapshot de la VM | A.5.28 | 8 min |
| Erradicación | Verifiqué que no quedaba ningún proceso de cifrado activo | A.5.26 | 12 min |
| Erradicación | Documenté el script cifrador y lo eliminé | A.5.26 | 20 min |
| Recuperación | Ejecuté `ransomware_decrypt.py` | A.5.26 | 2 h 13 min |
| Recuperación | Restauré los 6 archivos | A.5.29 | 2 h 14 min |
| Verificación | Confirmé la integridad de los archivos | A.5.26 | 2 h 20 min |

### Fase 4. Actividad posterior al incidente (ISO A.5.27)

- Redacté este reporte.
- Documenté los gaps con sus controles ISO.
- Ya había agregado los EID 11 y 23 de Sysmon y las reglas 100200 y 100210 antes de correr el ataque, para poder detectar el cifrado. No son una mejora posterior.
- Dejé las lecciones aprendidas en este reporte.
- El plan de mejora está en la sección 9.

---

## 5. Línea de tiempo (UTC)

| Hora | Fase | Evento |
|---|---|---|
| 23/08 22:13:38 | Detección | T1489: `sc.exe stop spooler` (reglas 92032/92052) |
| 23/08 22:58:48 | Detección | T1490: `vssadmin delete shadows` |
| 23/08 23:05:09 | Detección | T1490: `wbadmin delete catalog` |
| 24/08 00:57:31 | Detección | T1486: empieza el cifrado; primera alerta, regla 100200 (EID 11) |
| 24/08 00:57:32 | Detección | 13 alertas en total (6 de EID 11 y 7 de EID 23) |
| 24/08 01:02 | Contención | Endpoint aislado de la red |
| 24/08 01:05 | Contención | Snapshot de la VM |
| 24/08 01:09 | Erradicación | Verificación de que no había procesos de cifrado activos |
| 24/08 01:17 | Erradicación | Script cifrador documentado y eliminado |
| 24/08 03:10 | Recuperación | Ejecución de `ransomware_decrypt.py` |
| 24/08 03:11 | Recuperación | 6 archivos restaurados y notas de rescate eliminadas |
| 24/08 03:17 | Verificación | Integridad de los archivos confirmada |
| 24/08 03:30 | Post-incidente | Redacción de este reporte |

---

## 6. Indicadores de compromiso

| Tipo | Valor | Técnica |
|---|---|---|
| Proceso | `python.exe` (`C:\Program Files\Python312\`) | T1486 |
| Extensión | `.locked` | T1486 |
| Archivo dejado | `README_RECOVER.txt` | T1486 |
| Archivo | `decrypt_key.key` | T1486 |
| Comando | `vssadmin.exe delete shadows /all /quiet` | T1490 |
| Comando | `wbadmin delete catalog -quiet` | T1490 |
| Comando | `sc.exe stop spooler` | T1489 |

`vssadmin.exe` y `wbadmin.exe` son binarios legítimos de Windows, así que su hash no sirve como IoC. Los dejo como referencia para verificar su integridad:

| Binario | Hash |
|---|---|
| vssadmin.exe | MD5 `B58073DB8892B67A672906C9358020EC` |
| vssadmin.exe | SHA256 `8C1FABCC2196E4D096B7D155837C5F699AD7F55EDBF84571E4F8E03500B7A8B0` |
| wbadmin.exe | MD5 `151FEEFF52D82BFB150B80F852DC7B50` |
| wbadmin.exe | SHA256 `94235BD6D75B2B11243F47D7EA2B5958433CCDE58368C2C9F1B14226E68867F6` |

---

## 7. Impacto

| Categoría | Detalle |
|---|---|
| Archivos cifrados | 6 (`.txt` → `.txt.locked`), con Fernet (AES-128-CBC + HMAC-SHA256) |
| Carpetas afectadas | 3 (Finanzas, RRHH, Proyectos), todas con archivos señuelo |
| Shadow copies | Eliminadas (T1490-1) |
| Catálogo de backup | Eliminado (T1490-3) |
| Servicio detenido | Print Spooler (T1489-1) |
| Equipos afectados | 1 (DESKTOP-60HVTTB) |
| Datos exfiltrados | No detectado |
| Tiempo de recuperación | 2 horas 14 minutos |
| Pérdida de datos | 0, porque la clave estaba disponible |

---

## 8. Continuidad del negocio

Esta sección es un ejercicio de formato: el lab no tiene áreas ni sistemas de negocio reales, así que los objetivos y los responsables son supuestos.

### 8.1 Objetivos de recuperación

| Métrica | Qué mide | Objetivo supuesto | Valor en este incidente |
|---|---|---|---|
| RTO | Tiempo máximo para restaurar las operaciones | 4 horas | 2 h 14 min (cumplido) |
| RPO | Máxima pérdida de datos aceptable | 24 horas | 0 (la clave estaba disponible) |
| MTTR | Tiempo real de recuperación | Menor o igual al RTO | 2 h 14 min |

### 8.2 Análisis de impacto (BIA)

| Área o sistema | Clasificación | Criticidad | Estado durante el incidente | Control |
|---|---|---|---|---|
| Documentos de Finanzas | Confidencial | Alta | Cifrados (señuelo) | A.8.13 |
| Documentos de RRHH | Confidencial | Alta | Cifrados (señuelo) | A.8.13 |
| Documentos de Proyectos | Interno | Media | Cifrados (señuelo) | A.8.13 |
| Wazuh SIEM | Crítico | Máxima | Operativo | A.8.16 |
| Agente de monitoreo | Crítico | Máxima | Activo | A.8.16 |
| Backups offline | Crítico | Máxima | No configurados (gap) | A.8.13 |

### 8.3 Estrategia de continuidad (ISO A.5.29 y A.5.30)

Mientras el endpoint estuvo aislado, esto es lo que se haría en una organización real:

| Proceso afectado | Procedimiento alternativo | Responsable | Control |
|---|---|---|---|
| Acceso a documentos de Finanzas | Trabajo manual y escalado a IT para evaluar la recuperación | Finanzas | A.5.29 |
| Acceso a documentos de RRHH | Trabajo manual con copias locales | RRHH | A.5.29 |
| Operaciones del endpoint | Reasignación temporal | IT | A.5.29 |
| Comunicación interna | Canal alternativo fuera del dominio | IT | A.5.29 |
| Aviso a los interesados | Dentro de los 30 minutos de confirmado el incidente | CISO | A.6.8 |

Árbol de comunicación (ISO A.6.8):

```
T+0   Detección automática (Wazuh SIEM)
T+5   El analista SOC confirma y escala al equipo de respuesta
T+15  Aviso al CISO o responsable de seguridad
T+30  Primer aviso a la gerencia
T+60  Evaluación del alcance y decisión de recuperación
T+2h  Actualización de estado a los interesados
T+Xh  Cierre del incidente (ISO A.5.27)
```

### 8.4 Pruebas del plan de continuidad (ISO A.5.30)

| Actividad | Frecuencia | Responsable | Control |
|---|---|---|---|
| Simulacro de ransomware (tabletop) | Anual | CISO y SOC | A.5.24 |
| Prueba de restauración desde backup offline | Trimestral | IT / SysAdmin | A.8.13 |
| Revisión del runbook de respuesta | Semestral | Analista SOC senior | A.5.24 |
| Actualización de reglas de detección | Después de cada incidente y trimestral | Analista SOC | A.8.16 |
| Verificación de RTO y RPO contra operaciones reales | Semestral | CISO y negocio | A.5.30 |
| Auditoría interna de controles ISO 27001 | Anual | Auditor interno | Cláusula 9.2 |

---

## 9. Gaps y plan de mejora (ISO/IEC 27001, cláusula 10.2)

### Gap 1. EID 7036 sin recolectar (A.8.16)
El canal `System` no está configurado en `ossec.conf`, así que el servicio detenido (T1489) no llegó al SIEM.
**Acción:** agregar el canal `System` al agente de Wazuh.
**Prioridad:** alta · **Responsable:** analista SOC · **Plazo:** 7 días

### Gap 2. Detección genérica para T1489 y T1490 (A.5.25)
Las tres técnicas se clasificaron como T1059.003 y no como T1489 o T1490. El SIEM no identificó la preparación del ransomware.
**Acción:** reglas propias para `vssadmin`, `wbadmin` y `sc.exe` con argumentos destructivos.
**Prioridad:** alta · **Responsable:** analista SOC · **Plazo:** 14 días

### Gap 3. EID 23 deshabilitado en Sysmon (A.8.16)
FileDelete estaba comentado en la config base de SwiftOnSecurity y tuve que habilitarlo a mano.
**Acción:** revisar la config de Sysmon según cada caso de uso.
**Prioridad:** media · **Responsable:** analista SOC · **Plazo:** 14 días

### Gap 4. Sin correlación previa al ataque (A.5.25)
T1489 y T1490 ocurrieron más de dos horas antes del cifrado y no generaron una alerta combinada de "preparación de ransomware".
**Acción:** regla de correlación: T1489 y T1490 en menos de 60 minutos generan una alerta de nivel 14.
**Prioridad:** alta · **Responsable:** analista SOC · **Plazo:** 30 días

### Gap 5. Sin backup offline (A.8.13)
Con las shadow copies borradas, el sistema se quedó sin recuperación nativa. Recuperé gracias a la clave en manos del "atacante". Sin ella, la pérdida de datos habría sido total.
**Acción:** backup offline (air-gapped) con un RPO de 4 horas.
**Prioridad:** crítica · **Responsable:** IT / SysAdmin · **Plazo:** inmediato

### Gap 6. Sin política para scripts de Python (A.8.7)
`python.exe` se ejecutó sin restricciones en el endpoint.
**Acción:** revisar la política de ejecución de aplicaciones o aplicar allowlisting.
**Prioridad:** media · **Responsable:** IT · **Plazo:** 30 días

### Gap 7. Sin árbol de notificación formal (A.6.8)
No existe un procedimiento escrito de escalado y notificación para incidentes de seguridad.
**Acción:** definir el árbol de comunicación y una plantilla de aviso.
**Prioridad:** media · **Responsable:** CISO · **Plazo:** 30 días

---

## 10. Recomendaciones priorizadas

| Prioridad | Control | Recomendación |
|---|---|---|
| Crítica | A.8.13 | Backup offline (air-gapped) con RPO de 4 horas |
| Alta | A.5.25 | Reglas propias para T1489 y T1490 |
| Alta | A.8.16 | Canal `System` en el agente de Wazuh (EID 7036) |
| Alta | A.5.25 | Regla de correlación de T1489 y T1490 como pre-alerta |
| Media | A.8.16 | Agregar `python.exe` al monitoreo de EID 1 en Sysmon |
| Media | A.5.30 | Formalizar RTO y RPO por sistema antes del próximo ejercicio |
| Media | A.5.24 | Programar un simulacro tabletop anual de ransomware |
| Media | A.6.8 | Definir el árbol de comunicación y de escalado |
| Baja | A.8.7 | Revisar la política de ejecución de scripts en los endpoints |
| Baja | A.8.8 | Revisar periódicamente las vulnerabilidades técnicas |

---

## 11. Referencias a ISO/IEC 27001:2022

Estas son las cláusulas y los controles que usé como guía, y dónde aparecen en el reporte:

| Referencia | Descripción | Dónde se refleja |
|---|---|---|
| Cláusula 6.1.2 | Evaluación de riesgos | BIA y tabla de impacto (secciones 7 y 8.2) |
| Cláusula 8.2 | Evaluación de riesgos de la información | Gaps y plan de mejora (sección 9) |
| Cláusula 9.1 | Seguimiento y medición | RTO, RPO y MTTR (sección 8.1) |
| Cláusula 10.2 | Mejora continua | Acciones correctivas (sección 9) |
| Anexo A, A.5.24 a A.5.30 | Gestión de incidentes y continuidad | Secciones 4, 5 y 8 |
| Anexo A, A.6.8 | Notificación de eventos | Árbol de comunicación (sección 8.3) |
| Anexo A, A.8.7 | Protección contra malware | Gap 6 (sección 9) |
| Anexo A, A.8.13 | Copia de seguridad | Gap 5 (sección 9) |
| Anexo A, A.8.16 | Monitoreo | Detección con Wazuh y Sysmon (secciones 4 y 5) |

---

## 12. Limitaciones del ejercicio

- La clave quedó en el mismo equipo, algo que un atacante real no haría. Eso hizo trivial la recuperación.
- Mis reglas 100200 y 100210 dependen de la extensión `.locked` y de `python.exe`. Detectan este simulador, no una familia real.
- No simulé persistencia, movimiento lateral ni exfiltración, y hubo un solo endpoint.
- No ejercité la notificación a terceros ni la continuidad del negocio: la sección 8 muestra el formato, no algo que haya ocurrido.

---

## 13. Firmas y aprobación

| Rol | Nombre | Fecha | Firma |
|---|---|---|---|
| Analista SOC (autor) | Braian Fernandez | 24/08/2026 | |
| Revisor de seguridad | | | |
| CISO / aprobador | | | |
| Responsable del SGSI | | | |

---

**Tipo de documento:** reporte de laboratorio (público)
**Próxima revisión:** a los 90 días del cierre o ante un incidente similar
**Marcos:** ISO/IEC 27001:2022 · NIST SP 800-61 · MITRE ATT&CK
**Versión:** 1.0
