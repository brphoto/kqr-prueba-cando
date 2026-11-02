# Prueba técnica Senior Odoo Developer
## Decisiones
- El SSCC usa la compañía activa al crear el paquete, porque un paquete vacío aún no tiene `company_id` calculada.
- Cada compañía obtiene una secuencia independiente y el serial ocupa los dígitos restantes del SSCC.
- El dígito de extensión es 0, la unicidad se garantiza en PostgreSQL y un prefijo ausente detiene la creación con un mensaje claro.
## Uso de IA
- Usé ChatGPT para revisar el enunciado, contrastar APIs de Odoo 19 y proponer una primera implementación y casos de prueba.
- Revisé manualmente el modelo `stock.package`, la utilidad GS1, las vistas, la lógica multiempresa y cada archivo generado.
## Pendiente
- No se incluyen la etiqueta PDF ni la migración de paquetes existentes porque están fuera del alcance indicado.
- Con más tiempo probaría concurrencia en la creación inicial de secuencias y añadiría traducciones.
## Tests
- Comando: `..\python\python.exe .\odoo-bin -c .\odoo.conf -d kqr_sscc_test --addons-path=odoo\addons,C:\Users\Bryan\Desktop\kqr-prueba-cando -i bc_sscc_palet --test-enable --test-tags=/bc_sscc_palet --stop-after-init --without-demo --logfile=C:\Users\Bryan\Desktop\kqr-prueba-cando\odoo-test.log`
- Resultado: 5 casos ejecutados, 0 fallos y 0 errores.
