# Especificación Técnica: Firma Electrónica I-9 con OTP

**Documento de implementación para integrar en aplicación de solicitud de empleo existente**

> Este documento es una especificación técnica completa para implementar firma electrónica del Formulario I-9 de USCIS cumpliendo con **8 CFR 274a.2** y la **ESIGN Act**. No constituye asesoría legal — debe ser revisado por abogado especializado en derecho migratorio antes de uso en producción.

---

## Tabla de contenidos

1. [Contexto y objetivo](#1-contexto-y-objetivo)
2. [Arquitectura general del flujo](#2-arquitectura-general-del-flujo)
3. [Flujo detallado paso a paso](#3-flujo-detallado-paso-a-paso)
4. [Estructura de datos para auditoría](#4-estructura-de-datos-para-auditoría)
5. [Almacenamiento y seguridad](#5-almacenamiento-y-seguridad)
6. [Cumplimiento de requisitos del DHS](#6-cumplimiento-de-requisitos-específicos-del-dhs)
7. [Endpoints API necesarios](#7-endpoints-api-necesarios)
8. [Procesos batch y mantenimiento](#8-procesos-batch-y-mantenimiento)
9. [Consideraciones de UX](#9-consideraciones-de-ux-para-empleados-de-restaurante)
10. [Stack tecnológico sugerido](#10-stack-tecnológico-sugerido)
11. [Testing y validación](#11-testing-y-validación)
12. [Integración con aplicación existente](#12-integración-con-aplicación-existente)
13. [Pendientes legales antes de producción](#13-pendientes-legales-antes-de-producción)

---

## 1. Contexto y objetivo

Implementar un módulo de firma electrónica para el Formulario I-9 de USCIS que cumpla con **8 CFR 274a.2** y la **ESIGN Act**, integrable en una aplicación de solicitud de empleo ya existente.

El módulo debe soportar:
- Firma del empleado (Sección 1)
- Firma del empleador o representante autorizado (Sección 2)
- Autenticación por OTP de doble canal (email + SMS)
- Captura de garabato en canvas con metadatos biométricos
- Audit trail inmutable y tamper-evident

**Cumplimiento objetivo:** sobrevivir una auditoría de ICE bajo las reglas reclasificadas de marzo 2026, donde fallas en sistemas electrónicos de I-9 son violaciones sustantivas sin período de cura. Multas hasta **$2,789 por formulario**.

---

## 2. Arquitectura general del flujo

```
[Aplicación existente] 
    ↓
[Módulo I-9: pre-llenado de datos]
    ↓
[Verificación de identidad: email + celular + OTP]
    ↓
[Presentación del I-9 + attestation checkbox]
    ↓
[Captura de firma: canvas con metadatos biométricos]
    ↓
[Sellado: hash SHA-256 + timestamp + audit trail]
    ↓
[Almacenamiento cifrado + indexación]
    ↓
[Confirmación al empleado + retención 3 años / 1 año post-terminación]
```

---

## 3. Flujo detallado paso a paso

### Paso 1 — Inicio de sesión I-9 (empleado)

**Trigger:** empleado completa solicitud de empleo y recibe oferta aceptada. La app existente lanza el módulo I-9.

**Datos requeridos del sistema existente:**
- ID único del empleado en la app
- Nombre legal completo
- Email verificado
- Número de celular verificado
- Fecha de inicio de empleo (start date)
- Entidad legal contratante
- Ubicación física de trabajo

**Acciones del módulo:**
- Crear registro `i9_session` con UUID v4
- Pre-llenar datos conocidos en el formulario I-9 (Sección 1)
- Generar token JWT de sesión (expiración: 30 minutos)
- Registrar evento `session_started` en audit log

### Paso 2 — Verificación de identidad multi-factor

**Implementación:**

```
2.1 Sistema envía OTP de 6 dígitos al EMAIL del empleado
    - Vigencia: 10 minutos
    - Algoritmo: TOTP o random criptográfico (no secuencial)
    - Almacenar hash bcrypt del OTP, no el OTP en texto plano

2.2 Empleado ingresa OTP de email → validación

2.3 Sistema envía OTP separado al CELULAR (SMS)
    - Mismo estándar que email OTP
    - Diferente código (no reutilizar)

2.4 Empleado ingresa OTP de SMS → validación

2.5 Sistema marca identidad como "verificada multi-canal"
```

**Justificación regulatoria:** 8 CFR 274a.2(i)(2) requiere "create and preserve a record verifying the identity of the person producing the signature". El doble canal crea evidencia robusta de control sobre dos medios independientes.

**Eventos en audit log:** `otp_email_sent`, `otp_email_verified`, `otp_sms_sent`, `otp_sms_verified` con timestamps, IPs, intentos fallidos.

### Paso 3 — Presentación del formulario I-9

**Acciones:**
- Renderizar I-9 versión vigente (actualmente edición 01/20/25, válida hasta 05/31/2027)
- **CRÍTICO:** No alterar nombre, contenido, ni secuencia de campos. No insertar campos adicionales (8 CFR 274a.2(e))
- Verificar contra `https://www.uscis.gov/i-9` periódicamente para nuevas ediciones
- Permitir al empleado revisar y corregir todos los campos pre-llenados
- Mostrar instrucciones oficiales del I-9 disponibles para descarga

### Paso 4 — Attestation y consentimiento ESIGN

**Pantalla de consentimiento ESIGN (requerido antes de la firma):**

Texto obligatorio (en inglés y español, el empleado elige):
- Consentimiento explícito a hacer negocios electrónicamente
- Derecho a recibir copia en papel del documento
- Derecho a retirar consentimiento (con consecuencias)
- Requisitos de hardware/software para acceder a registros
- Cómo actualizar información de contacto

**Checkboxes obligatorios (todos deben marcarse):**

```
☐ He leído las instrucciones del Formulario I-9
☐ Entiendo que estoy firmando bajo pena de perjurio (28 USC §1746)
☐ Consiento usar firma electrónica para este documento
☐ Confirmo que la información en la Sección 1 es verdadera y correcta
```

**Registrar:** estado de cada checkbox individualmente, timestamp de cada uno.

### Paso 5 — Captura de firma (canvas)

**Especificación técnica del canvas:**

```javascript
{
  width: 600,  // mínimo en px
  height: 200, // mínimo en px
  background: 'white',
  strokeColor: 'black',
  strokeWidth: 2.5,
  
  // Captura biométrica del trazo
  capture: {
    points: [{x, y, timestamp_ms, pressure}],
    totalStrokes: number,
    durationMs: number,
    boundingBox: {x, y, width, height}
  },
  
  // Validación
  minStrokes: 1,
  minPixelsCovered: 0.05, // 5% del área
  minDurationMs: 500
}
```

**Outputs del componente:**
1. Imagen PNG de la firma (base64 o blob)
2. SVG vectorial de la firma (para escalabilidad)
3. JSON de datos biométricos del trazo (puntos x/y/t)
4. Hash SHA-256 de la firma renderizada

**Opciones alternativas que debes ofrecer:**
- "Dibujar firma" (canvas) — opción principal
- "Escribir nombre" (fuente cursiva tipo Dancing Script) — fallback accesibilidad
- "Subir imagen de firma" (PNG/JPG, máx 500KB) — fallback

### Paso 6 — Sellado del documento

**Proceso de sellado (server-side, atómico):**

```
6.1 Generar PDF final del I-9 con firma incrustada visualmente
6.2 Calcular hash SHA-256 del PDF resultante
6.3 Crear "evidence package" (JSON) con todos los metadatos
6.4 Calcular hash SHA-256 del evidence package
6.5 Concatenar: hash_pdf + hash_evidence + timestamp_utc
6.6 Firmar concatenación con clave privada del servidor (RSA-2048 o Ed25519)
6.7 Almacenar firma criptográfica como "tamper seal"
6.8 Opcional pero recomendado: enviar hash a servicio de timestamping 
    RFC 3161 o blockchain notary para prueba de existencia en el tiempo
```

**Justificación:** crea evidencia tamper-evident. Si alguien modifica el PDF posteriormente, el hash no coincidirá y el sello quedará invalidado.

### Paso 7 — Sección 2 (empleador / representante autorizado)

**Flujo paralelo dentro de 3 días hábiles del start date:**

- Representante autorizado del empleador examina físicamente (o vía procedimiento alternativo DHS si aplica E-Verify) los documentos de identidad presentados
- Mismo proceso de OTP doble canal para el representante
- Mismo proceso de attestation y firma
- Sistema marca el I-9 como `completed` solo cuando ambas secciones tienen firma válida

### Paso 8 — Confirmación y entrega

**Al completarse:**
- Email automático al empleado con: PDF firmado, evidence package resumido, instrucciones para solicitar copia impresa
- Email al empleador con: PDF firmado y notificación de cumplimiento
- Marcar registro en BD como `status: completed, locked: true`
- Bloquear edición del registro (solo lectura desde este punto)

---

## 4. Estructura de datos para auditoría

### 4.1 Tabla principal `i9_records`

```sql
CREATE TABLE i9_records (
  id UUID PRIMARY KEY,
  employee_id UUID NOT NULL,
  employer_entity_id UUID NOT NULL,
  
  -- Versionado del formulario
  form_edition_date VARCHAR(10) NOT NULL,    -- ej: "01/20/25"
  form_expiration_date VARCHAR(10) NOT NULL, -- ej: "05/31/2027"
  
  -- Estados
  status VARCHAR(50) NOT NULL, -- 'draft', 'section1_signed', 'section2_signed', 'completed', 'voided'
  hire_date DATE NOT NULL,
  termination_date DATE,
  retention_until DATE NOT NULL, -- max(hire+3yr, termination+1yr)
  
  -- Documentos
  pdf_storage_path VARCHAR(500) NOT NULL,
  pdf_sha256 VARCHAR(64) NOT NULL,
  evidence_package_path VARCHAR(500) NOT NULL,
  evidence_sha256 VARCHAR(64) NOT NULL,
  tamper_seal_signature TEXT NOT NULL,
  
  -- Timestamps
  created_at TIMESTAMP WITH TIME ZONE NOT NULL,
  section1_signed_at TIMESTAMP WITH TIME ZONE,
  section2_signed_at TIMESTAMP WITH TIME ZONE,
  completed_at TIMESTAMP WITH TIME ZONE,
  locked BOOLEAN DEFAULT FALSE
);

CREATE INDEX idx_i9_employee ON i9_records(employee_id);
CREATE INDEX idx_i9_status_retention ON i9_records(status, retention_until);
CREATE INDEX idx_i9_hire_date ON i9_records(hire_date);
```

### 4.2 Tabla `i9_signatures`

```sql
CREATE TABLE i9_signatures (
  id UUID PRIMARY KEY,
  i9_record_id UUID NOT NULL REFERENCES i9_records(id),
  signer_role VARCHAR(50) NOT NULL, -- 'employee', 'employer', 'preparer_translator'
  signer_user_id UUID NOT NULL,
  signer_name_legal VARCHAR(255) NOT NULL,
  signer_email VARCHAR(255) NOT NULL,
  signer_phone VARCHAR(50) NOT NULL,
  
  -- Método de firma
  signature_method VARCHAR(50) NOT NULL, -- 'canvas_draw', 'typed_cursive', 'uploaded_image'
  signature_image_path VARCHAR(500) NOT NULL,
  signature_svg_path VARCHAR(500),
  signature_biometric_data JSONB,
  signature_sha256 VARCHAR(64) NOT NULL,
  
  -- Contexto de firma
  signed_at TIMESTAMP WITH TIME ZONE NOT NULL, -- UTC con precisión ms
  ip_address INET NOT NULL,
  ip_geolocation JSONB,
  user_agent TEXT NOT NULL,
  device_fingerprint VARCHAR(255),
  session_id UUID NOT NULL,
  
  -- Verificación de identidad
  identity_verification_id UUID NOT NULL REFERENCES identity_verifications(id),
  
  -- Attestations
  attestation_read_instructions BOOLEAN NOT NULL,
  attestation_perjury_acknowledged BOOLEAN NOT NULL,
  attestation_esign_consent BOOLEAN NOT NULL,
  attestation_info_correct BOOLEAN NOT NULL,
  
  CONSTRAINT all_attestations_required CHECK (
    attestation_read_instructions = TRUE AND
    attestation_perjury_acknowledged = TRUE AND
    attestation_esign_consent = TRUE AND
    attestation_info_correct = TRUE
  )
);
```

### 4.3 Tabla `identity_verifications`

```sql
CREATE TABLE identity_verifications (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL,
  verification_type VARCHAR(50) NOT NULL, -- 'multi_channel_otp'
  
  -- OTP Email
  email_address VARCHAR(255) NOT NULL,
  email_otp_hash VARCHAR(255) NOT NULL, -- bcrypt
  email_otp_sent_at TIMESTAMP WITH TIME ZONE NOT NULL,
  email_otp_verified_at TIMESTAMP WITH TIME ZONE,
  email_otp_attempts INT DEFAULT 0,
  
  -- OTP SMS
  phone_number VARCHAR(50) NOT NULL,
  sms_otp_hash VARCHAR(255) NOT NULL,
  sms_otp_sent_at TIMESTAMP WITH TIME ZONE NOT NULL,
  sms_otp_verified_at TIMESTAMP WITH TIME ZONE,
  sms_otp_attempts INT DEFAULT 0,
  sms_carrier_info JSONB,
  
  -- Resultado
  fully_verified BOOLEAN DEFAULT FALSE,
  verified_at TIMESTAMP WITH TIME ZONE,
  
  -- Auditoría
  created_at TIMESTAMP WITH TIME ZONE NOT NULL,
  ip_address INET NOT NULL
);
```

### 4.4 Tabla `i9_audit_log` (append-only, immutable)

```sql
CREATE TABLE i9_audit_log (
  id BIGSERIAL PRIMARY KEY,
  i9_record_id UUID NOT NULL,
  event_type VARCHAR(100) NOT NULL,
  event_data JSONB NOT NULL,
  
  actor_user_id UUID,
  actor_role VARCHAR(50),
  
  ip_address INET,
  user_agent TEXT,
  session_id UUID,
  
  occurred_at TIMESTAMP WITH TIME ZONE NOT NULL,
  
  -- Hash chain para inmutabilidad
  previous_event_hash VARCHAR(64),
  this_event_hash VARCHAR(64) NOT NULL
);

-- Trigger que prohibe modificación
CREATE OR REPLACE FUNCTION prevent_audit_modification()
RETURNS TRIGGER AS $$
BEGIN
  RAISE EXCEPTION 'Audit log is immutable - UPDATE/DELETE forbidden';
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER audit_log_immutable
BEFORE UPDATE OR DELETE ON i9_audit_log
FOR EACH ROW EXECUTE FUNCTION prevent_audit_modification();
```

**Eventos a registrar (lista exhaustiva):**

```
session_started, session_expired, session_resumed
form_loaded, form_field_changed, form_validation_failed
otp_email_sent, otp_email_verified, otp_email_failed, otp_email_resent
otp_sms_sent, otp_sms_verified, otp_sms_failed, otp_sms_resent
esign_consent_shown, esign_consent_accepted, esign_consent_declined
attestation_checkbox_marked, attestation_checkbox_unmarked
signature_canvas_started, signature_canvas_completed, signature_canvas_cleared
signature_method_changed, signature_submitted
document_sealed, hash_calculated, tamper_seal_applied
section1_completed, section2_completed, i9_completed
document_viewed, document_downloaded, document_printed
correction_requested, correction_applied
ice_inspection_export, retention_review, scheduled_destruction
```

### 4.5 Estructura del Evidence Package (JSON)

```json
{
  "version": "1.0",
  "i9_record_id": "uuid",
  "form_edition": "01/20/25",
  "completed_at_utc": "2026-05-06T14:32:18.452Z",
  
  "employee": {
    "legal_name": "...",
    "employee_id": "uuid",
    "hire_date": "2026-05-15",
    "employer_entity": "Entity Legal Name LLC"
  },
  
  "section1_signature": {
    "signer_name": "...",
    "method": "canvas_draw",
    "signed_at_utc": "...",
    "ip_address": "...",
    "ip_geolocation": {},
    "user_agent": "...",
    "device_fingerprint": "...",
    "signature_sha256": "...",
    "biometric_summary": {
      "stroke_count": 4,
      "duration_ms": 2341,
      "bounding_box": {}
    },
    "identity_verification": {
      "method": "multi_channel_otp",
      "email_verified_at": "...",
      "sms_verified_at": "...",
      "email_used": "***@example.com",
      "phone_last_4": "1234"
    },
    "attestations": {
      "read_instructions": {"value": true, "timestamp": "..."},
      "perjury_acknowledged": {"value": true, "timestamp": "..."},
      "esign_consent": {"value": true, "timestamp": "..."},
      "info_correct": {"value": true, "timestamp": "..."}
    }
  },
  
  "section2_signature": { },
  
  "document_integrity": {
    "pdf_sha256": "...",
    "evidence_sha256": "...",
    "tamper_seal_algorithm": "Ed25519",
    "tamper_seal_signature": "...",
    "tamper_seal_public_key_id": "...",
    "rfc3161_timestamp": "..."
  },
  
  "system_metadata": {
    "application_version": "...",
    "form_template_hash": "...",
    "server_timezone": "UTC",
    "retention_until": "2030-05-15"
  }
}
```

---

## 5. Almacenamiento y seguridad

### 5.1 Cifrado

- **En tránsito:** TLS 1.3 obligatorio en todos los endpoints
- **En reposo:** AES-256-GCM para PDFs y evidence packages
- **Claves de cifrado:** gestionadas por KMS (AWS KMS, Azure Key Vault, o HashiCorp Vault)
- **Rotación:** claves de firma rotadas anualmente, claves anteriores retenidas para verificación histórica

### 5.2 Estructura de almacenamiento de archivos

```
s3://your-bucket-i9-records/
  └── {year}/
      └── {employer_entity_id}/
          └── {employee_id}/
              └── {i9_record_id}/
                  ├── form_signed.pdf
                  ├── evidence_package.json
                  ├── tamper_seal.bin
                  ├── section1_signature.png
                  ├── section1_signature.svg
                  ├── section2_signature.png
                  └── identity_documents/
                      ├── list_a_doc1.pdf
                      ├── list_b_doc.pdf
                      └── list_c_doc.pdf
```

**Configuración S3 (o equivalente):**
- Object Lock en modo Compliance (no se puede eliminar antes de retention_until)
- Versionado habilitado
- Replicación cross-region para disaster recovery
- Logs de acceso a CloudTrail

### 5.3 Control de acceso (RBAC)

```
Roles mínimos:
- i9_admin:     lectura/escritura completa, no puede eliminar
- i9_hr_user:   lectura de registros de su entidad asignada
- i9_employee:  lectura de su propio I-9 únicamente
- i9_auditor:   lectura completa, sin escritura (para ICE)
- i9_destroyer: única role con permiso de eliminación post-retention
```

**Logs de acceso:** todo acceso a un I-9 (lectura, descarga, impresión) se registra en `i9_audit_log` con evento `document_viewed`.

---

## 6. Cumplimiento de requisitos específicos del DHS

Checklist de verificación contra 8 CFR 274a.2:

| Requisito | Implementación |
|---|---|
| Acknowledgment of attestation | Checkbox obligatorio + log |
| Signature attached to form | PDF con firma incrustada + hash binding |
| Signature affixed at transaction time | Timestamp UTC con ms en momento de submit |
| Identity verification record | Tabla `identity_verifications` con OTP doble canal |
| Printed confirmation on request | Endpoint `/i9/{id}/print-confirmation` |
| Section 2 attestation acknowledgment | Checkbox separado para empleador |
| Reasonable controls vs. alteration | Tamper seal + Object Lock + audit log inmutable |
| Quality assurance program | Job programado de verificación de hashes mensual |
| Indexing system | Índices SQL + búsqueda full-text |
| Reproduce legible paper copies | Endpoint de descarga PDF con visualización completa |
| Records security program | KMS, RBAC, MFA admin, logs de acceso |
| 3-year/1-year retention | Campo `retention_until` + Object Lock |
| 72-hour ICE response | Endpoint de exportación masiva con filtros |

---

## 7. Endpoints API necesarios

```
POST   /api/i9/sessions                          # Iniciar I-9
GET    /api/i9/sessions/{id}                     # Obtener estado
POST   /api/i9/sessions/{id}/otp/email/send
POST   /api/i9/sessions/{id}/otp/email/verify
POST   /api/i9/sessions/{id}/otp/sms/send
POST   /api/i9/sessions/{id}/otp/sms/verify
POST   /api/i9/sessions/{id}/esign-consent
PATCH  /api/i9/sessions/{id}/form-data           # Actualizar campos
POST   /api/i9/sessions/{id}/section1/sign       # Firmar empleado
POST   /api/i9/sessions/{id}/section2/sign       # Firmar empleador
GET    /api/i9/records/{id}/pdf                  # Descargar PDF firmado
GET    /api/i9/records/{id}/evidence             # Descargar evidence package
GET    /api/i9/records/{id}/audit-trail          # Ver audit log
POST   /api/i9/records/{id}/print-confirmation
POST   /api/i9/admin/ice-export                  # Exportación masiva auditoría
POST   /api/i9/admin/integrity-check             # Verificar tamper seals
```

---

## 8. Procesos batch y mantenimiento

### 8.1 Verificación de integridad mensual

Job programado que recalcula hashes de cada PDF y los compara contra `pdf_sha256` almacenado. Cualquier discrepancia se loguea como evento crítico y se notifica al equipo de cumplimiento.

### 8.2 Gestión de retención

Job diario que identifica registros con `retention_until` vencido (90 días de aviso). Notifica al `i9_admin` para revisión antes de programar destrucción. La destrucción real requiere aprobación manual de dos personas (4-eyes principle).

### 8.3 Actualización de versión del formulario

Cuando USCIS publica nueva edición del I-9, los registros existentes mantienen su versión original (no se migran). Solo nuevos I-9 usan la nueva versión. El sistema debe permitir que coexistan múltiples versiones del template.

---

## 9. Consideraciones de UX para empleados de restaurante

Dado el contexto típico (alta rotación, primer empleo común, dispositivos móviles, posibles dificultades con inglés):

- **Mobile-first:** todo el flujo debe funcionar perfectamente en pantallas de 375px de ancho
- **Bilingüe completo:** inglés y español disponibles en cada paso, switch persistente
- **Guardado automático:** estado de la sesión guardado cada 30 segundos
- **Resumibilidad:** si el OTP expira o se cierra el navegador, el empleado puede retomar con un nuevo OTP
- **Validación inline:** errores mostrados al lado del campo, no al final
- **Indicadores de progreso:** barra de pasos visible siempre
- **Soporte humano:** botón "necesito ayuda" que envía notificación a HR

---

## 10. Stack tecnológico sugerido

Ajustar según el stack actual de la aplicación existente:

- **Backend:** Node.js + Express, Python + FastAPI, o Ruby on Rails
- **Base de datos:** PostgreSQL 15+ (soporte nativo JSONB, generated columns, hash chain triggers)
- **Almacenamiento:** AWS S3 con Object Lock, o equivalente (Azure Blob con Immutable Storage, GCS con Bucket Lock)
- **Cifrado:** AWS KMS o HashiCorp Vault
- **OTP SMS:** Twilio Verify, AWS SNS, o MessageBird
- **OTP Email:** SendGrid, AWS SES, o Postmark
- **Generación PDF:** PDFKit, ReportLab, o llenado de PDF template existente con pdf-lib
- **Canvas firma:** signature_pad.js (frontend) o equivalente
- **Timestamping RFC 3161:** FreeTSA o servicio comercial como DigiCert
- **Frontend:** React/Vue/Angular con captura de canvas táctil

---

## 11. Testing y validación

Casos de prueba críticos antes de producción:

1. Firma exitosa con todos los attestations marcados
2. Intento de firma con attestations incompletos (debe rechazar)
3. OTP expirado (debe regenerar)
4. OTP con código incorrecto 5 veces (debe bloquear)
5. Intento de modificar PDF post-firma (tamper seal debe detectar)
6. Intento de eliminar registro pre-retention (Object Lock debe bloquear)
7. Exportación masiva para auditoría ICE (debe completarse en menos de 72hr)
8. Verificación de integridad con un hash corrupto (debe alertar)
9. Cambio de idioma a mitad del flujo (estado debe persistir)
10. Sesión interrumpida y resumida desde otro dispositivo

---

## 12. Integración con aplicación existente

### 12.1 Análisis previo necesario

Antes de comenzar la implementación, mapea lo siguiente en la aplicación existente:

- **Modelo de usuario actual:** ¿qué campos ya existen (email, teléfono, nombre legal)?
- **Sistema de autenticación:** ¿usa JWT, sesiones, OAuth?
- **Sistema de roles/permisos:** ¿hay RBAC implementado?
- **Stack de almacenamiento:** ¿qué se usa para archivos actualmente?
- **Sistema de notificaciones:** ¿qué proveedores de email/SMS ya están conectados?
- **Logging y observabilidad:** ¿hay un sistema centralizado (Datadog, Sentry, ELK)?

### 12.2 Estrategia de integración recomendada

**Opción A — Módulo embebido (recomendado para apps monolíticas):**
- Crear un namespace/módulo dentro de la aplicación existente: `/i9/`
- Reutilizar el modelo de usuario existente
- Compartir la misma BD pero con tablas separadas con prefijo `i9_`
- Reutilizar autenticación pero agregar capa adicional de OTP solo para firma I-9

**Opción B — Microservicio separado (para apps complejas):**
- Servicio independiente con su propia BD
- Comunicación vía API REST con la app principal
- Webhooks para notificar eventos a la app principal
- Mejor aislamiento de cumplimiento, pero mayor complejidad operacional

### 12.3 Pasos de implementación incremental

**Fase 1 — Fundación (Semanas 1-2):**
1. Crear migraciones de base de datos para las 4 tablas principales
2. Implementar el modelo de datos en el ORM/framework existente
3. Configurar almacenamiento (S3 con Object Lock o equivalente)
4. Configurar KMS para cifrado
5. Configurar proveedores de OTP (Twilio + SendGrid o equivalentes)

**Fase 2 — Backend core (Semanas 3-4):**
6. Implementar endpoints de sesión I-9
7. Implementar lógica de OTP doble canal
8. Implementar lógica de attestations
9. Implementar generación de PDF con firma incrustada
10. Implementar tamper sealing y evidence packages
11. Implementar audit log con hash chain

**Fase 3 — Frontend (Semanas 5-6):**
12. Implementar UI del flujo I-9 con i18n (EN/ES)
13. Integrar componente de canvas de firma
14. Implementar pantallas de OTP
15. Implementar pantalla de attestations
16. Implementar visualización de PDF firmado

**Fase 4 — Sección 2 y workflows administrativos (Semana 7):**
17. Implementar flujo de firma del empleador
18. Implementar paneles administrativos para HR
19. Implementar exportación para ICE

**Fase 5 — Procesos batch y testing (Semana 8):**
20. Implementar jobs de verificación de integridad
21. Implementar jobs de gestión de retención
22. Ejecutar suite completa de testing
23. Auditoría de seguridad externa
24. Revisión legal final

### 12.4 Variables de entorno necesarias

```bash
# Storage
I9_S3_BUCKET=
I9_S3_REGION=
I9_S3_KMS_KEY_ID=

# OTP Providers
I9_TWILIO_ACCOUNT_SID=
I9_TWILIO_AUTH_TOKEN=
I9_TWILIO_VERIFY_SERVICE_SID=
I9_SENDGRID_API_KEY=
I9_OTP_FROM_EMAIL=
I9_OTP_FROM_NAME=

# Cryptography
I9_TAMPER_SEAL_PRIVATE_KEY_KMS_ID=
I9_TAMPER_SEAL_PUBLIC_KEY=
I9_RFC3161_TSA_URL=

# Application
I9_FORM_TEMPLATE_PATH=
I9_FORM_EDITION_DATE=01/20/25
I9_FORM_EXPIRATION_DATE=05/31/2027
I9_SESSION_TIMEOUT_MINUTES=30
I9_OTP_EXPIRATION_MINUTES=10
I9_OTP_MAX_ATTEMPTS=5

# Compliance
I9_AUDIT_RETENTION_YEARS=7
I9_ENABLE_RFC3161_TIMESTAMP=true
```

### 12.5 Checklist de integración

Antes de habilitar producción, verificar:

- [ ] Todas las tablas creadas con índices apropiados
- [ ] Triggers de inmutabilidad en audit log probados
- [ ] Object Lock configurado y probado en bucket
- [ ] Cifrado en reposo verificado (todos los archivos cifrados)
- [ ] TLS 1.3 enforcement en todos los endpoints
- [ ] Roles RBAC creados y asignados correctamente
- [ ] OTP doble canal funcionando con providers reales
- [ ] PDF generado idéntico al template oficial USCIS (sin cambios)
- [ ] Tamper seal verificable después de generación
- [ ] Audit log captura todos los eventos listados
- [ ] Export para ICE funciona con datos de prueba
- [ ] Job de verificación de integridad ejecuta correctamente
- [ ] Flujo móvil probado en iOS y Android (varios browsers)
- [ ] Flujo bilingüe verificado por hablantes nativos
- [ ] Documentación de operaciones para HR creada
- [ ] Plan de respuesta a auditoría ICE documentado
- [ ] Backup y disaster recovery probados
- [ ] Revisión legal completada
- [ ] Auditoría de seguridad externa completada

---

## 13. Pendientes legales antes de producción

Antes de lanzar a producción, **obtén revisión de:**

- **Abogado especializado en inmigración / I-9 compliance** — revisión del flujo completo, attestations, y documentación
- **Auditor SOC 2** si planeas certificación corporativa
- **Privacy officer** para cumplimiento con leyes de privacidad estatales (FIPA en Florida, CCPA en California, etc.)
- **Broker de seguros** sobre coverage de errores y omisiones (E&O insurance)
- **DPO** si manejas empleados con datos protegidos por GDPR (poco común en I-9 pero posible)

---

## Referencias regulatorias

- **8 CFR 274a.2** — Reglamentos de DHS sobre completado, firma electrónica y almacenamiento del Formulario I-9
- **ESIGN Act (15 USC §7001 et seq.)** — Ley federal de firmas electrónicas
- **UETA** — Uniform Electronic Transactions Act (adoptada por 49 estados)
- **28 USC §1746** — Declaración bajo pena de perjurio (texto del attestation)
- **USCIS Form I-9** — `https://www.uscis.gov/i-9`
- **Handbook for Employers M-274** — `https://www.uscis.gov/i-9-central/form-i-9-resources/handbook-for-employers-m-274`
- **ICE Form I-9 Inspection Fact Sheet (Marzo 2026)** — guía actualizada de violaciones sustantivas vs. técnicas

---

**Última actualización del documento:** mayo 2026  
**Versión del Formulario I-9 referenciada:** edición 01/20/25 (válida hasta 05/31/2027)

> ⚠️ **Disclaimer:** Este documento es una especificación técnica y no constituye asesoría legal. Las regulaciones de USCIS/DHS pueden cambiar. La implementación debe ser revisada por abogado calificado en derecho migratorio antes de su uso en producción. Las multas por incumplimiento bajo las reglas de ICE de marzo 2026 pueden alcanzar $2,789 por formulario y ahora se clasifican como violaciones sustantivas sin período de cura.
