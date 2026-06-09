% ============================================================
% Doctor Byte - Base de Conocimiento
% Sistema experto para diagnóstico de fallas en computadoras
% ============================================================


% ============================================================
% SÍNTOMAS
% Formato: sintoma(id).
% ============================================================

sintoma(pantalla_negra).
sintoma(pantalla_azul).
sintoma(reinicio_inesperado).
sintoma(lentitud_extrema).
sintoma(no_enciende).
sintoma(sobrecalentamiento).
sintoma(ruido_disco).
sintoma(no_detecta_disco).
sintoma(error_arranque).
sintoma(sin_imagen).
sintoma(congelamiento).
sintoma(no_reconoce_usb).
sintoma(wifi_no_conecta).
sintoma(bateria_no_carga).
sintoma(ventilador_ruidoso).
sintoma(aplicaciones_se_cierran).
sintoma(memoria_insuficiente).


% ============================================================
% DESCRIPCIÓN LEGIBLE DE SÍNTOMAS
% Formato: descripcion_sintoma(id, 'Descripción').
% ============================================================

descripcion_sintoma(pantalla_negra,          'La pantalla está completamente negra al encender').
descripcion_sintoma(pantalla_azul,           'Aparece una pantalla azul con código de error (BSOD)').
descripcion_sintoma(reinicio_inesperado,     'El equipo se reinicia solo sin previo aviso').
descripcion_sintoma(lentitud_extrema,        'El sistema responde muy lento o tarda en ejecutar tareas básicas').
descripcion_sintoma(no_enciende,             'El equipo no enciende ni emite señales de vida').
descripcion_sintoma(sobrecalentamiento,      'El equipo se calienta demasiado durante el uso').
descripcion_sintoma(ruido_disco,             'Se escuchan ruidos extraños o chasquidos desde el disco duro').
descripcion_sintoma(no_detecta_disco,        'El sistema no detecta el disco duro en el arranque').
descripcion_sintoma(error_arranque,          'Aparece un error al intentar iniciar el sistema operativo').
descripcion_sintoma(sin_imagen,              'El monitor no muestra imagen aunque el equipo parece encendido').
descripcion_sintoma(congelamiento,           'El sistema se congela y no responde al teclado ni al ratón').
descripcion_sintoma(no_reconoce_usb,         'El equipo no detecta dispositivos conectados por USB').
descripcion_sintoma(wifi_no_conecta,         'No es posible conectarse a redes WiFi').
descripcion_sintoma(bateria_no_carga,        'La batería no carga o pierde carga muy rápido').
descripcion_sintoma(ventilador_ruidoso,      'El ventilador hace un ruido excesivo o inusual').
descripcion_sintoma(aplicaciones_se_cierran, 'Las aplicaciones se cierran solas de forma inesperada').
descripcion_sintoma(memoria_insuficiente,    'Aparecen mensajes de memoria insuficiente con frecuencia').


% ============================================================
% FALLAS DIAGNOSTICABLES
% Formato: falla(id).
% ============================================================

falla(falla_disco_duro).
falla(falla_ram).
falla(falla_gpu).
falla(falla_fuente_poder).
falla(sobrecarga_termica).
falla(falla_sistema_operativo).
falla(falla_controlador_usb).
falla(falla_tarjeta_red).
falla(falla_bateria).
falla(infeccion_malware).
falla(falla_placa_madre).


% ============================================================
% DESCRIPCIÓN LEGIBLE DE FALLAS
% Formato: descripcion_falla(id, 'Descripción').
% ============================================================

descripcion_falla(falla_disco_duro,        'Falla en el disco duro').
descripcion_falla(falla_ram,               'Problema con la memoria RAM').
descripcion_falla(falla_gpu,               'Problema con la tarjeta gráfica').
descripcion_falla(falla_fuente_poder,      'Problema con la fuente de poder').
descripcion_falla(sobrecarga_termica,      'Sobrecalentamiento del procesador').
descripcion_falla(falla_sistema_operativo, 'Corrupción del sistema operativo').
descripcion_falla(falla_controlador_usb,   'Falla en los controladores USB').
descripcion_falla(falla_tarjeta_red,       'Problema con la tarjeta de red inalámbrica').
descripcion_falla(falla_bateria,           'Batería dañada o agotada').
descripcion_falla(infeccion_malware,       'Infección por malware o virus').
descripcion_falla(falla_placa_madre,       'Problema con la placa madre').


% ============================================================
% RECOMENDACIONES POR FALLA
% Formato: recomendacion(id_falla, 'Texto de recomendación').
% Una falla puede tener múltiples recomendaciones.
% ============================================================

recomendacion(falla_disco_duro, 'Realiza un respaldo inmediato de tus datos importantes').
recomendacion(falla_disco_duro, 'Verifica el estado del disco con herramientas como CrystalDiskInfo').
recomendacion(falla_disco_duro, 'Revisa que los cables SATA estén bien conectados').
recomendacion(falla_disco_duro, 'Considera reemplazar el disco duro si los errores persisten').

recomendacion(falla_ram, 'Retira y vuelve a insertar los módulos de RAM').
recomendacion(falla_ram, 'Prueba cada módulo de RAM por separado para identificar el defectuoso').
recomendacion(falla_ram, 'Ejecuta MemTest86 para verificar errores en la memoria').
recomendacion(falla_ram, 'Reemplaza el módulo de RAM dañado si las pruebas fallan').

recomendacion(falla_gpu, 'Actualiza los drivers de la tarjeta gráfica').
recomendacion(falla_gpu, 'Verifica que la tarjeta gráfica esté bien insertada en el slot PCIe').
recomendacion(falla_gpu, 'Comprueba la temperatura de la GPU con GPU-Z').

recomendacion(falla_fuente_poder, 'Verifica que el cable de poder esté bien conectado').
recomendacion(falla_fuente_poder, 'Prueba con otra fuente de poder si es posible').
recomendacion(falla_fuente_poder, 'Reemplaza la fuente de poder si no entrega voltaje estable').

recomendacion(sobrecarga_termica, 'Limpia el polvo acumulado en los ventiladores y disipadores').
recomendacion(sobrecarga_termica, 'Reemplaza la pasta térmica del procesador').
recomendacion(sobrecarga_termica, 'Asegúrate de que el equipo tenga ventilación adecuada').
recomendacion(sobrecarga_termica, 'Verifica que todos los ventiladores estén funcionando correctamente').

recomendacion(falla_sistema_operativo, 'Ejecuta el comando sfc /scannow para reparar archivos del sistema').
recomendacion(falla_sistema_operativo, 'Intenta reparar el sistema operativo desde el medio de instalación').
recomendacion(falla_sistema_operativo, 'Como último recurso considera reinstalar el sistema operativo').

recomendacion(falla_controlador_usb, 'Actualiza los drivers USB desde el administrador de dispositivos').
recomendacion(falla_controlador_usb, 'Prueba el dispositivo USB en otro puerto o en otra computadora').
recomendacion(falla_controlador_usb, 'Desinstala y reinstala los controladores USB desde el sistema').

recomendacion(falla_tarjeta_red, 'Actualiza los drivers de la tarjeta de red inalámbrica').
recomendacion(falla_tarjeta_red, 'Restablece la configuración de red del sistema operativo').
recomendacion(falla_tarjeta_red, 'Verifica que el servicio de red esté activo en el sistema').

recomendacion(falla_bateria, 'Calibra la batería descargándola completamente y recargándola').
recomendacion(falla_bateria, 'Verifica el estado de la batería con herramientas del fabricante').
recomendacion(falla_bateria, 'Reemplaza la batería si su capacidad es inferior al 40%').

recomendacion(infeccion_malware, 'Ejecuta un análisis completo con tu antivirus actualizado').
recomendacion(infeccion_malware, 'Descarga y ejecuta Malwarebytes para una segunda opinión').
recomendacion(infeccion_malware, 'Mantén el sistema operativo y aplicaciones siempre actualizados').
recomendacion(infeccion_malware, 'Evita descargar software de fuentes no oficiales o desconocidas').

recomendacion(falla_placa_madre, 'Inspecciona visualmente la placa madre en busca de capacitores dañados').
recomendacion(falla_placa_madre, 'Verifica que todos los conectores internos estén correctamente colocados').
recomendacion(falla_placa_madre, 'Consulta a un técnico especializado para un diagnóstico avanzado').


% ============================================================
% REGLAS DE INFERENCIA BÁSICAS
% Formato: diagnostico(ListaSintomas, Falla).
% Se activan cuando los síntomas indicados están en la lista.
% ============================================================

diagnostico(Sintomas, falla_disco_duro) :-
    member(ruido_disco, Sintomas),
    member(no_detecta_disco, Sintomas).

diagnostico(Sintomas, falla_disco_duro) :-
    member(ruido_disco, Sintomas),
    member(error_arranque, Sintomas).

diagnostico(Sintomas, falla_ram) :-
    member(pantalla_azul, Sintomas),
    member(reinicio_inesperado, Sintomas).

diagnostico(Sintomas, falla_ram) :-
    member(congelamiento, Sintomas),
    member(memoria_insuficiente, Sintomas).

diagnostico(Sintomas, falla_gpu) :-
    member(sin_imagen, Sintomas),
    member(pantalla_negra, Sintomas).

diagnostico(Sintomas, falla_fuente_poder) :-
    member(no_enciende, Sintomas),
    member(pantalla_negra, Sintomas).

diagnostico(Sintomas, sobrecarga_termica) :-
    member(sobrecalentamiento, Sintomas),
    member(ventilador_ruidoso, Sintomas).

diagnostico(Sintomas, sobrecarga_termica) :-
    member(sobrecalentamiento, Sintomas),
    member(reinicio_inesperado, Sintomas).

diagnostico(Sintomas, falla_sistema_operativo) :-
    member(error_arranque, Sintomas),
    member(pantalla_azul, Sintomas).

diagnostico(Sintomas, falla_sistema_operativo) :-
    member(error_arranque, Sintomas),
    member(congelamiento, Sintomas).

diagnostico(Sintomas, falla_controlador_usb) :-
    member(no_reconoce_usb, Sintomas).

diagnostico(Sintomas, falla_tarjeta_red) :-
    member(wifi_no_conecta, Sintomas).

diagnostico(Sintomas, falla_bateria) :-
    member(bateria_no_carga, Sintomas),
    member(no_enciende, Sintomas).

diagnostico(Sintomas, infeccion_malware) :-
    member(lentitud_extrema, Sintomas),
    member(aplicaciones_se_cierran, Sintomas).

diagnostico(Sintomas, infeccion_malware) :-
    member(lentitud_extrema, Sintomas),
    member(memoria_insuficiente, Sintomas).

diagnostico(Sintomas, falla_placa_madre) :-
    member(no_enciende, Sintomas),
    member(sobrecalentamiento, Sintomas),
    member(pantalla_negra, Sintomas).


% ============================================================
% REGLAS AVANZADAS
% Uso de corte (!), listas, variables y consultas encadenadas.
% ============================================================

% Devuelve el primer diagnóstico encontrado y detiene la búsqueda.
% El corte (!) evita que Prolog siga buscando más soluciones
% una vez que encontró la primera coincidencia.
primer_diagnostico(Sintomas, Falla) :-
    diagnostico(Sintomas, Falla), !.

% Cuenta cuántos síntomas de una lista están presentes en ListaSintomas.
% Usa corte (!) para no contar el mismo síntoma dos veces.
contar_coincidencias([], _, 0).
contar_coincidencias([S|Resto], ListaSintomas, Total) :-
    member(S, ListaSintomas), !,
    contar_coincidencias(Resto, ListaSintomas, Subtotal),
    Total is Subtotal + 1.
contar_coincidencias([_|Resto], ListaSintomas, Total) :-
    contar_coincidencias(Resto, ListaSintomas, Total).

% Verifica que todos los síntomas de una lista son válidos en el sistema.
todos_sintomas_validos([]).
todos_sintomas_validos([S|Resto]) :-
    sintoma(S),
    todos_sintomas_validos(Resto).

% Reúne todas las recomendaciones de una falla en una lista.
todas_recomendaciones(Falla, Lista) :-
    findall(R, recomendacion(Falla, R), Lista).

% Reúne todos los diagnósticos posibles dados los síntomas, sin duplicados.
todos_diagnosticos(Sintomas, Lista) :-
    findall(F, diagnostico(Sintomas, F), ListaConDuplicados),
    list_to_set(ListaConDuplicados, Lista).

% Genera el diagnóstico completo: falla + lista de recomendaciones.
% Encadena primer_diagnostico y todas_recomendaciones en una sola consulta.
diagnostico_completo(Sintomas, Falla, Recomendaciones) :-
    todos_sintomas_validos(Sintomas),
    primer_diagnostico(Sintomas, Falla),
    todas_recomendaciones(Falla, Recomendaciones).
