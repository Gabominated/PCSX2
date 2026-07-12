# PS2 Conditional Patching Guide for PCSX2 (.pnach)

Conditional codes in the PNACH format allow you to automatically enable or disable patches based on real-time game states (for example: enable 60fps only during gameplay and disable it during cutscenes or menus). This guide explains the two main conditional methods used by PCSX2: E-type and D-type codes. Both require the `extended` write type — short/word writes do not process these conditionals correctly.

---

## 1. E-Type Conditionals (E00XNNNN) — Multi-Line Evaluation

E-type codes evaluate the last 2 bytes (16 bits) of a memory address and conditionally apply multiple lines placed directly below the conditional line.

Syntax

```
patch=1,EE,E00XNNNN,extended,AAAAAAAA
patch=1,EE,YZZZZZZZ,extended,VVVVVVVV
```

- AAAAAAAA: Target memory address used as the trigger.
- NNNN: Specific 4-digit hex value expected at that address to trigger the patch (last 2 bytes).
- X: Number of physical lines directly beneath the conditional line that will be affected.
- Y: Write type for the target patch (0 = 1 byte, 1 = 2 bytes, 2 = 4 bytes/full value).

Practical example: Automatic FPS toggle (Gameplay vs Menus)

Suppose Cheat Engine found address `002AB59C` that reads `00000001` during gameplay and `00000000` in menus. We want to clear the game's default frame limiter value (`1040FFFA`) and write `00000000` to enable 60fps during gameplay, then restore the original value in menus.

```
// IF address 002AB59C equals 0001 (Gameplay), execute the next 1 line:
patch=1,EE,E0010001,extended,002AB59C
patch=1,EE,201195A4,extended,00000000  // Enable 60fps

// IF address 002AB59C equals 0000 (Menus/Pause), execute the next 1 line:
patch=1,EE,E0010000,extended,002AB59C
patch=1,EE,201195A4,extended,1040FFFA  // Restore native game value
```

Notes

- When using `E00X...`, be precise with the line count: `E002` affects exactly the next two physical lines. Do not insert blank lines or comments inside that block — the parser counts physical lines.
- Use `extended` write type for correct behavior.

---

## 2. D-Type Conditionals (DAAAAAAA) — 32-bit Evaluation (Single Line)

D-type codes evaluate the full 4 bytes (32 bits) of an address. Unlike E-type codes, a D-type conditional affects strictly the single line immediately below it. This is commonly used for monitoring controller states, engine flags, or other 32-bit status values.

Syntax

```
patch=1,EE,DAAAAAAA,extended,XXXXXXXX
patch=1,EE,YYYYYYYY,extended,VVVVVVVV
```

- AAAAAAAA: Memory address to monitor (note: D-type format omits the leading zero of an 8-digit address — the `D` replaces that leading zero).
- XXXXXXXX: The full 32-bit value required to execute the patch below.

Practical example: Dynamic 60fps control (Kingdom Hearts)

In this example (by Michael P), D-type lines are used to force the frame registration address (`002B624C`) to either `00000000` (enabled) or `00000001` (disabled) depending on engine states read at `002BFD98`.

```
gametitle=Kingdom Hearts [SLUS-20370] (U)
comment=60fps toggle cheat by Michael P

// ---- [60fps] TOGGLE ON (Gameplay) ----
// If address 002BFD98 matches any of these gameplay values, write 00000000 to 002B624C
patch=1,EE,D02BFD98,extended,00000000
patch=1,EE,002B624C,extended,00000000
patch=1,EE,D02BFD98,extended,00001000
patch=1,EE,002B624C,extended,00000000
patch=1,EE,D02BFD98,extended,00000020
patch=1,EE,002B624C,extended,00000000
patch=1,EE,D02BFD98,extended,00000001
patch=1,EE,002B624C,extended,00000000

// ---- [60fps] TOGGLE OFF (Cutscenes, FMV, and Scripted Events) ----
// If the address changes to loading or engine video states, restore the original value to avoid bugs
patch=1,EE,D02BFD98,extended,00000040
patch=1,EE,002B624C,extended,00000001
patch=1,EE,D02BFD98,extended,0000004E
patch=1,EE,002B624C,extended,00000001
patch=1,EE,D02BFD98,extended,00000004
patch=1,EE,002B624C,extended,00000001
```

---

## Golden rules to remember

- E-line counting precision: `E00X` counts physical lines. Avoid comments or blank lines between the conditional and its affected lines.
- State reversion: When a conditional modifies a value, always add the inverse conditional sequence to restore the game's natural value when the trigger no longer applies.
- Use `extended` writes for conditional logic to work reliably.
- Test thoroughly to avoid introducing gameplay bugs; conditional patches that don't correctly revert values can cause crashes or corruption.

---

## (Español)

# Guía de parches condicionales en PCSX2 (.pnach)

Los códigos condicionales en formato PNACH permiten activar o desactivar parches automáticamente en función del estado real del juego (por ejemplo: activar 60fps solo durante el gameplay y desactivarlo en cinemáticas o menús). Esta guía explica los dos métodos principales usados en PCSX2: códigos tipo E y tipo D. Ambos requieren el modo `extended` — los tipos `word` o `byte` no procesan estas condicionales correctamente.

---

## 1. Condicionales tipo E (E00XNNNN) — Evaluación multilínea

Los códigos tipo E evalúan los últimos 2 bytes (16 bits) de una dirección de memoria y aplican condicionalmente varias líneas que se encuentran directamente debajo de la línea condicional.

Sintaxis

```
patch=1,EE,E00XNNNN,extended,AAAAAAAA
patch=1,EE,YZZZZZZZ,extended,VVVVVVVV
```

- AAAAAAAA: Dirección de memoria usada como disparador (trigger).
- NNNN: Valor hex de 4 dígitos que debe tener esa dirección para activar el parche (últimos 2 bytes).
- X: Número de líneas físicas justo debajo de la condicional que se verán afectadas.
- Y: Tipo de escritura del parche (0 = 1 byte, 1 = 2 bytes, 2 = 4 bytes/valor completo).

Ejemplo práctico: Alternar FPS automáticamente (Gameplay vs Menús)

Supongamos que Cheat Engine encuentra `002AB59C` que vale `00000001` en el gameplay y `00000000` en los menús. Queremos escribir `00000000` para activar 60fps durante el gameplay y restaurar `1040FFFA` en los menús.

```
// SI la dirección 002AB59C vale 0001 (Gameplay), aplica la siguiente 1 línea:
patch=1,EE,E0010001,extended,002AB59C
patch=1,EE,201195A4,extended,00000000  // Activa 60fps

// SI la dirección 002AB59C vale 0000 (Menús/Pausa), aplica la siguiente 1 línea:
patch=1,EE,E0010000,extended,002AB59C
patch=1,EE,201195A4,extended,1040FFFA  // Restaura el valor nativo del juego
```

Notas

- Precisión en el conteo de E: `E00X` afecta exactamente las siguientes X líneas físicas. No inserte líneas vacías ni comentarios entre la condicional y el bloque de parches.
- Use `extended` para un comportamiento fiable.

---

## 2. Condicionales tipo D (DAAAAAAA) — Evaluación de 32 bits (línea única)

Los códigos tipo D evalúan los 4 bytes completos (32 bits) de una dirección. A diferencia del tipo E, un `D` solo afecta la línea inmediatamente debajo. Se usa habitualmente para estados de controlador, flags del motor o valores de 32 bits.

Sintaxis

```
patch=1,EE,DAAAAAAA,extended,XXXXXXXX
patch=1,EE,YYYYYYYY,extended,VVVVVVVV
```

- AAAAAAAA: Dirección a monitorear (el formato D omite el cero inicial de direcciones de 8 dígitos).
- XXXXXXXX: Valor de 32 bits que activará la línea siguiente.

Ejemplo práctico: Control dinámico de 60fps (Kingdom Hearts)

En este ejemplo (por Michael P), se usan líneas `D` para forzar la dirección `002B624C` a `00000000` (activado) o `00000001` (desactivado) según los estados leídos en `002BFD98`.

```
gametitle=Kingdom Hearts [SLUS-20370] (U)
comment=60fps toggle cheat by Michael P

// ---- [60fps] ACTIVAR (Gameplay) ----
patch=1,EE,D02BFD98,extended,00000000
patch=1,EE,002B624C,extended,00000000
... (líneas de ejemplo similares a la versión en inglés) ...

// ---- [60fps] DESACTIVAR (Cinemáticas, FMV y Eventos) ----
patch=1,EE,D02BFD98,extended,00000040
patch=1,EE,002B624C,extended,00000001
... (líneas de ejemplo similares a la versión en inglés) ...
```

---

## Reglas de oro

- Conteo en E: `E00X` cuenta líneas físicas; no deje comentarios ni líneas vacías dentro del bloque.
- Reversión de estado: si un parche modifica un valor, siempre provea la secuencia inversa para restaurar el valor natural cuando la condición deje de cumplirse.
- Use `extended` para que las condicionales funcionen correctamente.
- Pruebe a fondo: las condicionales mal formadas pueden causar comportamientos indeseados o bugs.

---

Si quieres que también renombre el archivo, añada un índice, o elimine alguna de las secciones en uno de los idiomas, dime y lo hago.