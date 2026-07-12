PS2 Conditional Patching Guide for PCSX2 (.pnach)

Conditional codes in the PNACH format allow you to automatically enable or disable patches based on real-time game states (e.g., enabling 60fps only during gameplay and disabling it during cutscenes to prevent speed bugs).

There are two primary engine methods to achieve this: E-type and D-type codes. Both methods require using the extended type; types like word or byte do not process these conditional logic rules correctly.

1. E-Type Conditionals (E00XNNNN) — Multi-Line Evaluation
The E-type code evaluates the last 2 bytes (16 bits) of a memory address and conditions multiple lines of code placed directly beneath it.

Syntax:
Plaintext
patch=1,EE,E00XNNNN,extended,AAAAAAAA
patch=1,EE,YZZZZZZZ,extended,VVVVVVVV
AAAAAAAA: The target memory address acting as the trigger.

NNNN: The specific 4-digit hex value you expect that address to hold to trigger the patch.

X: The number of physical lines directly below the conditional line that will be affected.

Y: The write type for the target patch (0 for 1 byte, 1 for 2 bytes, 2 for 4 bytes/full value).

Practical Example: Automatic FPS Toggle (Gameplay vs. Menus)
Suppose you used Cheat Engine to find a memory address (002AB59C) that reads 00000001 during gameplay and resets to 00000000 inside menus. We want to clear the game's default frame limiter value (1040FFFA) by overwriting it with 00000000.

Plaintext
// IF address 002AB59C equals 0001 (Gameplay), execute the next 1 line:
patch=1,EE,E0010001,extended,002AB59C
patch=1,EE,201195A4,extended,00000000 // Enable 60fps

// IF address 002AB59C equals 0000 (Menus/Pause), execute the next 1 line:
patch=1,EE,E0010000,extended,002AB59C
patch=1,EE,201195A4,extended,1040FFFA // Restore native game value
2. D-Type Conditionals (DAAAAAAA) — 32-bit Evaluation (Single Line)
The D-type code evaluates the full 4 bytes (32 bits) of an address. Unlike the E-type, it strictly affects only the single line immediately below it. It is typically used for monitoring controller button inputs or specific engine flags requiring full 32-bit precision.

Syntax:
Plaintext
patch=1,EE,DAAAAAAA,extended,XXXXXXXX
patch=1,EE,YYYYYYYY,extended,VVVVVVVV
AAAAAAA: The memory address to monitor (Note: the format drops the first leading zero of the 8-digit address to accommodate the "D").

XXXXXXXX: The full 32-bit value required to execute the patch below.

Practical Example: Dynamic 60fps Control (Kingdom Hearts)
In this script by Michael P, D-type lines are used to force the frame registration address (002B624C) to either 0 (enabled) or 1 (disabled) depending on the exact engine states reflected in address 002BFD98.

Plaintext
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

📌 Golden Rules to Remember
E-Line Counting Precision: If you use E002, the cheat engine strictly reads the next two physical lines. Do not leave blank lines or plain text comments inside that block; the parser will count them as lines of code and break your conditional logic sequence.

State Reversion: When using a conditional trigger to modify a value, always remember to write the inverse conditional sequence (reverting back to the game's natural value) so the engine resets properly when the gameplay state changes.

(Español)
Guía de Parches Condicionales en PCSX2 (.pnach)

Los códigos condicionales en el formato PNACH permiten activar o desactivar parches automáticamente según lo que esté ocurriendo en el juego (por ejemplo, activar los 60fps solo durante el gameplay y desactivarlos en cinemáticas para evitar bugs de velocidad).

Existen dos métodos principales para lograr esto: los tipos E y D. Ambos requieren trabajar en modo extended (los tipos word o byte no procesan estas condicionales correctamente).

1. Condicionales tipo E (E00XNNNN) — Evaluación Multilínea
El código tipo E evalúa los últimos 2 bytes (16 bits) de una dirección de memoria y puede condicionar múltiples líneas de código que se encuentren debajo de él.

Sintaxis:
Plaintext
patch=1,EE,E00XNNNN,extended,AAAAAAAA
patch=1,EE,YZZZZZZZ,extended,VVVVVVVV
AAAAAAAA: La dirección de memoria que actúa como activador (trigger).

NNNN: El valor específico (en 4 dígitos hex) que esperas que tome esa dirección para activar el truco.

X: El número de líneas físicas que se encuentran justo debajo y que se verán afectadas por la condición.

Y: El tipo de escritura para el parche que se va a aplicar (0 para 1 byte, 1 para 2 bytes, 2 para 4 bytes/valor completo).

Ejemplo Práctico: Automatización de FPS (Gameplay vs. Menús)
Supongamos que encontraste una dirección con Cheat Engine (002AB59C) que vale 00000001 en el gameplay y 00000000 en los menús. Queremos cambiar el valor natural del juego (1040FFFA) a 00000000 para liberar los frames.

Plaintext
// SI la dirección 002AB59C toma valor 0001 (Gameplay), aplica la siguiente 1 línea:
patch=1,EE,E0010001,extended,002AB59C
patch=1,EE,201195A4,extended,00000000 // Activa 60fps

// SI la dirección 002AB59C toma valor 0000 (Menús/Pausa), aplica la siguiente 1 línea:
patch=1,EE,E0010000,extended,002AB59C
patch=1,EE,201195A4,extended,1040FFFA // Revierte al valor original del juego
2. Condicionales tipo D (DAAAAAAA) — Evaluación de 32 bits (Línea Única)
El código tipo D evalúa los 4 bytes completos (32 bits) de una dirección. A diferencia del tipo E, solo afecta estrictamente a la línea que tiene inmediatamente abajo. Se utiliza habitualmente para detectar combinaciones de botones (inputs del mando) o estados del motor que requieran precisión de 32 bits.

Sintaxis:
Plaintext
patch=1,EE,DAAAAAAA,extended,XXXXXXXX
patch=1,EE,YYYYYYYY,extended,VVVVVVVV
AAAAAAA: La dirección de memoria a monitorear (ojo: el formato omite el primer cero de la dirección de 8 dígitos para meter la "D").

XXXXXXXX: El valor completo de 32 bits que activará el truco.

Ejemplo Práctico: Control de 60fps dinámico (Kingdom Hearts)
En este script de Michael P, se usa el tipo D para forzar el registro de la tasa de frames (002B624C) a 0 (activado) o a 1 (desactivado) dependiendo del estado exacto del motor gráfico reflejado en la dirección 002BFD98.

Plaintext
gametitle=Kingdom Hearts [SLUS-20370] (U)
comment=60fps toggle cheat by Michael P

// ---- [60fps] TOGGLE ON (Gameplay) ----
// Si la dirección 002BFD98 tiene cualquiera de estos valores de gameplay, escribe 00000000 en 002B624C
patch=1,EE,D02BFD98,extended,00000000
patch=1,EE,002B624C,extended,00000000
patch=1,EE,D02BFD98,extended,00001000
patch=1,EE,002B624C,extended,00000000
patch=1,EE,D02BFD98,extended,00000020
patch=1,EE,002B624C,extended,00000000
patch=1,EE,D02BFD98,extended,00000001
patch=1,EE,002B624C,extended,00000000

// ---- [60fps] TOGGLE OFF (Cinemáticas, FMV y Eventos) ----
// Si la dirección cambia a estados de carga o video, reescribe el valor a 00000001 para evitar bugs
patch=1,EE,D02BFD98,extended,00000040
patch=1,EE,002B624C,extended,00000001
patch=1,EE,D02BFD98,extended,0000004E
patch=1,EE,002B624C,extended,00000001
patch=1,EE,D02BFD98,extended,00000004
patch=1,EE,002B624C,extended,00000001

📌 Resumen de Reglas de Oro
Regla de conteo en E: Si usas E002, necesitas tener exactamente dos líneas de código abajo. No dejes líneas vacías ni comentarios entre la condicional y los parches, ya que el emulador los contará como líneas físicas y romperá el truco.

Doble acción: Si usas una condicional para activar algo, recuerda siempre crear la condicional inversa (como en el ejemplo de los menús) para restaurar el valor original (natural) del juego cuando la condición deje de cumplirse.