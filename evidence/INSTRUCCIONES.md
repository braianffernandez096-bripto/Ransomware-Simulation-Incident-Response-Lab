# Guía de Capturas — Evidencias del Laboratorio

Esta carpeta contiene las capturas de pantalla del lab organizadas por técnica MITRE.
Los nombres de archivo ya están asignados y coinciden con las referencias del README.

---

## Archivos presentes y qué muestra cada uno

### T1489 — Stop Service

| Archivo | Qué muestra | Prioridad |
|---|---|---|
| `01-T1489-sc-cmdline-detalle.png` | Vista general Wazuh — 2 hits, lista con sc.exe y cmd.exe | Alta |
| `02-T1489-cadena-proceso-wazuh.png` | Documento expandido — commandLine `sc.exe stop spooler` resaltado + metadata | Alta |
| `03-T1489-rule92032-alerta.png` | Sección de regla — rule.id 92032, rule.description, rule.level | Alta |

### T1490 — Inhibit System Recovery (vssadmin)

| Archivo | Qué muestra | Prioridad |
|---|---|---|
| `04-T1490-vssadmin-cmdline-wazuh.png` | Documento expandido — commandLine `vssadmin.exe delete shadows /all /quiet` resaltado + hashes | Alta |
| `05-T1490-vssadmin-cadena-padre.png` | Proceso padre — commandLine `"cmd.exe" /c vssadmin delete shadows` resaltado | Alta |
| `06-T1490-vssadmin-rule-mitre.png` | Sección de regla — rule.id 92052, rule.mitre.id T1059.003, tactic Execution | Alta |

### T1490 — Inhibit System Recovery (wbadmin)

| Archivo | Qué muestra | Prioridad |
|---|---|---|
| `10-T1490-wbadmin-cmdline-wazuh.png` | Documento expandido — commandLine `wbadmin delete catalog -quiet` resaltado | Alta |
| `11-T1490-wbadmin-cadena-padre.png` | Proceso padre — commandLine `"cmd.exe" /c wbadmin delete catalog` resaltado | Alta |
| `12-T1490-wbadmin-rule92052-mitre.png` | Sección de regla — rule.id 92052, confirma patrón para wbadmin | Media |

### T1486 — Data Encrypted for Impact (cifrado)

| Archivo | Qué muestra | Prioridad |
|---|---|---|
| `07-T1486-ejecucion-python-encrypt.png` | Output completo de `ransomware_sim.py` en PowerShell — 6 archivos cifrados, clave guardada | Alta |
| `08-T1486-nota-rescate-readme-recover.png` | Explorador de archivos + Notepad con README_RECOVER.txt abierto | Alta |

### T1486 — Data Encrypted for Impact (detección Wazuh)

| Archivo | Qué muestra | Prioridad |
|---|---|---|
| `09-T1486-13hits-overview-wazuh.png` | Overview general — 13 hits en el gráfico, filtro rule.id 100200 OR 100210 | Alta |
| `15-T1486-rule100210-metadata-hashes.png` | Documento rule 100210 — archived:true, hashes, image python.exe, targetFilename .txt eliminado | Alta |
| `16-T1486-rule100210-groups-impact.png` | Sección regla 100210 — groups ransomware/t1486, rule.mail true, mitre T1486 Impact | Alta |
| `17-T1486-rule100200-filecreate-locked.png` | Documento rule 100200 — targetFilename .locked, image python.exe, ruleName T1486 | Alta |
| `18-T1486-rule100200-description-mitre.png` | Sección regla 100200 — description completo, rule.id, mitre T1486 Data Encrypted for Impact | Alta |

### Recuperación

| Archivo | Qué muestra | Prioridad |
|---|---|---|
| `13-Recuperacion-python-decrypt-output.png` | Output completo de `ransomware_decrypt.py` — 6 archivos restaurados, notas eliminadas | Alta |
| `14-Recuperacion-archivos-restaurados.png` | Explorador de archivos — carpeta Finanzas con .txt restaurados (sin .locked) | Alta |

---

## Resumen por técnica

| Archivo | Técnica | Prioridad |
|---|---|---|
| 01-T1489-sc-cmdline-detalle.png | T1489 | Alta |
| 02-T1489-cadena-proceso-wazuh.png | T1489 | Alta |
| 03-T1489-rule92032-alerta.png | T1489 | Alta |
| 04-T1490-vssadmin-cmdline-wazuh.png | T1490 | Alta |
| 05-T1490-vssadmin-cadena-padre.png | T1490 | Alta |
| 06-T1490-vssadmin-rule-mitre.png | T1490 | Alta |
| 07-T1486-ejecucion-python-encrypt.png | T1490 | Alta |
| 08-T1486-nota-rescate-readme-recover.png | T1490 | Alta |
| 09-T1486-archivos-locked-finanzas.png | T1490 | Media |
| 10-T1486-13hits-overview-wazuh.png | T1490 | Media |
| 11-T1490-wbadmin-cmdline-wazuh.png | T1486 | Alta |
| 12-T1490-wbadmin-cadena-padre.png | T1486 | Alta |
| 13-T1490-wbadmin-rule92052-mitre.png | T1486 | Alta |
| 14-Recuperacion-python-decrypt-output.png | T1486 | Alta |
| 15-Recuperacion-archivos-restaurados.png | T1486 | Alta |
| 16-T1486-rule100210-metadata-hashes.png | T1486 | Alta |
| 17-T1486-rule100210-groups-impact.png | T1486 | Alta |
| 18-T1486-rule100200-filecreate-locked.png | T1486 | Alta |
| 19-T1486-rule100200-description-mitree.png | T1486 | Alta |

**Total: 18 capturas — 17 Alta, 1 Media**
