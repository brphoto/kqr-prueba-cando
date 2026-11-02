# ¿Configurar o desarrollar?

## 1. Bloques predefinidos en presupuestos
Lo resolvería con un desarrollo pequeño que inserte una plantilla de líneas al final del pedido, sin aplicar una plantilla de presupuesto completa ni reemplazar líneas existentes.
Reutilizaría secciones, notas y productos de `sale.order.template.line`, conservando el orden y recalculando precios con la tarifa del presupuesto.
Preguntaría si el bloque debe poder editarse, si puede añadirse varias veces y cómo deben tratarse cantidades, descuentos e impuestos.

## 2. Lotes en el TPV
Primero usaría configuración estándar: desactivaría crear/usar lotes solo en el tipo de operación del TPV y mantendría la obligatoriedad en el tipo de operación de recepciones.
Esto elimina la pregunta en caja, pero también deja la salida del TPV sin lote; confirmaría si el cliente acepta perder esa trazabilidad en ventas.
Si necesita trazabilidad de salida sin intervención del cajero, propondría un módulo que asigne automáticamente el lote por FEFO.

## 3. Importación de NIF internacionales
No desactivaría globalmente la validación ni empezaría con un script: limpiaría el Excel e importaría primero país y después NIF en el formato esperado por `base_vat`.
Haría una importación piloto y usaría una transformación reproducible solo para normalizar prefijos, separadores o identificadores heredados.
Preguntaría por ejemplos rechazados, país y tipo de persona, y conservaría un informe de filas corregidas o pendientes.
