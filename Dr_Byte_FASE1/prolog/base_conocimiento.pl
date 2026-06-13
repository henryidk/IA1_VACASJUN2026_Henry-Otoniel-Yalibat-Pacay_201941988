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

descripcion_falla(falla_disco_duro,        'Falla en el disco duro o unidad de almacenamiento').
descripcion_falla(falla_ram,               'Problema con la memoria RAM').
descripcion_falla(falla_gpu,               'Problema con la tarjeta gráfica').
descripcion_falla(falla_fuente_poder,      'Problema con la fuente de alimentación').
descripcion_falla(sobrecarga_termica,      'Sobrecalentamiento del sistema').
descripcion_falla(falla_sistema_operativo, 'Corrupción o falla en el sistema operativo').
descripcion_falla(falla_controlador_usb,   'Falla en los controladores o puertos USB').
descripcion_falla(falla_tarjeta_red,       'Problema con la tarjeta o adaptador de red inalámbrica').
descripcion_falla(falla_bateria,           'Batería dañada, agotada o descalibrada').
descripcion_falla(infeccion_malware,       'Infección por malware, virus o software malicioso').
descripcion_falla(falla_placa_madre,       'Falla en la placa madre o chipset del sistema').


% ============================================================
% REGLAS DE INFERENCIA: RELACIÓN SÍNTOMA → FALLA
% Formato: sintoma_falla(Sintoma, Falla).
%
% Un síntoma puede apuntar a una o más fallas.
% El motor suma cuántos síntomas seleccionados apuntan a cada
% falla y elige la que mayor acumulado tenga.
%
% Síntomas exclusivos (apuntan a una sola falla):
%   garantizan ese diagnóstico cuando aparecen solos.
% Síntomas compartidos (apuntan a varias fallas):
%   necesitan combinarse para inclinar la balanza.
% falla_placa_madre solo acumula cuando varios síntomas
%   graves coinciden, evitando diagnósticos apresurados.
% ============================================================

% --- Síntomas exclusivos ---
% Ruido mecánico es inequívoco de disco fallando.
sintoma_falla(ruido_disco,        falla_disco_duro).

% USB no detectado → drivers o controlador, no la placa.
sintoma_falla(no_reconoce_usb,    falla_controlador_usb).

% WiFi sin conexión → adaptador o su driver.
sintoma_falla(wifi_no_conecta,    falla_tarjeta_red).

% Batería sin carga → batería degradada.
sintoma_falla(bateria_no_carga,   falla_bateria).

% Fan ruidoso → sistema disipando calor excesivo.
sintoma_falla(ventilador_ruidoso, sobrecarga_termica).

% --- Síntomas compartidos ---

% Pantalla negra: sin alimentación, GPU sin señal, o fallo total de hardware.
sintoma_falla(pantalla_negra, falla_fuente_poder).
sintoma_falla(pantalla_negra, falla_gpu).
sintoma_falla(pantalla_negra, falla_placa_madre).

% No enciende: fuente muerta, batería agotada (laptop), o placa sin vida.
sintoma_falla(no_enciende, falla_fuente_poder).
sintoma_falla(no_enciende, falla_bateria).
sintoma_falla(no_enciende, falla_placa_madre).

% BSOD: RAM defectuosa (causa #1) o archivos del SO corruptos.
sintoma_falla(pantalla_azul, falla_ram).
sintoma_falla(pantalla_azul, falla_sistema_operativo).

% Sin imagen: GPU sin señal, fuente insuficiente, o placa sin POST.
sintoma_falla(sin_imagen, falla_gpu).
sintoma_falla(sin_imagen, falla_fuente_poder).
sintoma_falla(sin_imagen, falla_placa_madre).

% Error de arranque: bootloader/MBR corrupto o disco con errores.
sintoma_falla(error_arranque, falla_sistema_operativo).
sintoma_falla(error_arranque, falla_disco_duro).

% Reinicio inesperado: apagado por temperatura o voltaje inestable.
sintoma_falla(reinicio_inesperado, sobrecarga_termica).
sintoma_falla(reinicio_inesperado, falla_fuente_poder).

% Congelamiento: throttling por calor o errores de RAM.
sintoma_falla(congelamiento, sobrecarga_termica).
sintoma_falla(congelamiento, falla_ram).

% Lentitud extrema: malware en segundo plano o disco envejecido.
sintoma_falla(lentitud_extrema, infeccion_malware).
sintoma_falla(lentitud_extrema, falla_disco_duro).

% Apps se cierran: OOM/RAM defectuosa o interferencia de malware.
sintoma_falla(aplicaciones_se_cierran, falla_ram).
sintoma_falla(aplicaciones_se_cierran, infeccion_malware).

% Memoria insuficiente: RAM dañada o malware consumiendo recursos.
sintoma_falla(memoria_insuficiente, falla_ram).
sintoma_falla(memoria_insuficiente, infeccion_malware).

% No detecta disco: disco desconectado o tabla de particiones dañada.
sintoma_falla(no_detecta_disco, falla_disco_duro).
sintoma_falla(no_detecta_disco, falla_sistema_operativo).

% Sobrecalentamiento: sistema térmico saturado o reguladores de voltaje de la placa.
sintoma_falla(sobrecalentamiento, sobrecarga_termica).
sintoma_falla(sobrecalentamiento, falla_placa_madre).


% ============================================================
% RECOMENDACIONES POR FALLA
% Ordenadas de menor a mayor impacto: lo más sencillo primero.
% Formato: recomendacion(id_falla, 'Texto').
% ============================================================

recomendacion(falla_disco_duro, 'Verifica que los cables SATA y de alimentación estén bien conectados').
recomendacion(falla_disco_duro, 'Realiza un respaldo inmediato de tus datos importantes').
recomendacion(falla_disco_duro, 'Analiza el estado del disco con CrystalDiskInfo o HD Sentinel').
recomendacion(falla_disco_duro, 'Reemplaza el disco si el análisis detecta sectores dañados').

recomendacion(falla_ram, 'Retira y vuelve a insertar correctamente los módulos de RAM').
recomendacion(falla_ram, 'Prueba cada módulo por separado para identificar el defectuoso').
recomendacion(falla_ram, 'Ejecuta MemTest86 para verificar errores en la memoria').
recomendacion(falla_ram, 'Reemplaza el módulo de RAM dañado si las pruebas detectan fallas').

recomendacion(falla_gpu, 'Verifica que el cable de video esté bien conectado al monitor').
recomendacion(falla_gpu, 'Actualiza los drivers de la tarjeta gráfica desde el sitio del fabricante').
recomendacion(falla_gpu, 'Verifica que la GPU esté bien insertada en el slot PCIe').
recomendacion(falla_gpu, 'Prueba con otra tarjeta gráfica para confirmar el origen de la falla').

recomendacion(falla_fuente_poder, 'Verifica que el cable de poder esté bien conectado al equipo').
recomendacion(falla_fuente_poder, 'Asegúrate de que el interruptor de la fuente esté en posición ON').
recomendacion(falla_fuente_poder, 'Prueba con otra fuente de poder de repuesto si es posible').
recomendacion(falla_fuente_poder, 'Reemplaza la fuente si no entrega voltaje estable al equipo').

recomendacion(sobrecarga_termica, 'Asegúrate de que el equipo esté en un lugar con buena ventilación').
recomendacion(sobrecarga_termica, 'Limpia el polvo acumulado en ventiladores y disipadores').
recomendacion(sobrecarga_termica, 'Verifica que todos los ventiladores del equipo estén funcionando').
recomendacion(sobrecarga_termica, 'Reemplaza la pasta térmica del procesador si el problema persiste').

recomendacion(falla_sistema_operativo, 'Reinicia el sistema en modo seguro para verificar estabilidad').
recomendacion(falla_sistema_operativo, 'Ejecuta sfc /scannow para reparar archivos del sistema').
recomendacion(falla_sistema_operativo, 'Repara el arranque desde el medio de instalación del sistema').
recomendacion(falla_sistema_operativo, 'Reinstala el sistema operativo como último recurso').

recomendacion(falla_controlador_usb, 'Prueba el dispositivo USB en otro puerto disponible del equipo').
recomendacion(falla_controlador_usb, 'Reinicia el sistema y vuelve a conectar el dispositivo').
recomendacion(falla_controlador_usb, 'Actualiza los controladores USB desde el Administrador de dispositivos').
recomendacion(falla_controlador_usb, 'Desinstala y reinstala los controladores USB desde el sistema').

recomendacion(falla_tarjeta_red, 'Activa y desactiva el WiFi desde el panel de red del sistema').
recomendacion(falla_tarjeta_red, 'Reinicia el router y acércate más al punto de acceso inalámbrico').
recomendacion(falla_tarjeta_red, 'Actualiza los controladores de la tarjeta de red inalámbrica').
recomendacion(falla_tarjeta_red, 'Restablece la configuración de red del sistema operativo').

recomendacion(falla_bateria, 'Verifica que el cargador esté bien conectado al equipo y al tomacorriente').
recomendacion(falla_bateria, 'Prueba con otro cargador compatible si tienes uno disponible').
recomendacion(falla_bateria, 'Calibra la batería: descárgala completamente y luego cárgala al 100%').
recomendacion(falla_bateria, 'Reemplaza la batería si su capacidad es inferior al 40%').

recomendacion(infeccion_malware, 'Ejecuta un análisis completo con tu antivirus actualizado').
recomendacion(infeccion_malware, 'Descarga y ejecuta Malwarebytes para una segunda opinión').
recomendacion(infeccion_malware, 'Actualiza el sistema operativo y todas las aplicaciones instaladas').
recomendacion(infeccion_malware, 'Evita descargar software de fuentes no oficiales o desconocidas').

recomendacion(falla_placa_madre, 'Verifica que todos los conectores internos estén bien colocados').
recomendacion(falla_placa_madre, 'Prueba con componentes mínimos: una RAM, sin GPU discreta').
recomendacion(falla_placa_madre, 'Inspecciona la placa en busca de capacitores dañados o quemados').
recomendacion(falla_placa_madre, 'Consulta a un técnico especializado para un diagnóstico avanzado').


% ============================================================
% MOTOR DE INFERENCIA POR CONTEO DE COINCIDENCIAS
% ============================================================

% Cuenta cuántos síntomas seleccionados apuntan a una falla.
% Solo tiene éxito si al menos un síntoma está asociado a esa falla.
puntaje_falla(Sintomas, Falla, Puntaje) :-
    falla(Falla),
    findall(1, (member(S, Sintomas), sintoma_falla(S, Falla)), Coincidencias),
    Coincidencias \= [],
    length(Coincidencias, Puntaje).

% Reúne todos los pares Puntaje-Falla para los síntomas dados.
todos_puntajes(Sintomas, Pares) :-
    findall(Puntaje-Falla, puntaje_falla(Sintomas, Falla, Puntaje), Pares).

% Selecciona la falla con mayor número de síntomas coincidentes.
% En caso de empate, elige la primera falla en orden de declaración.
% El corte (!) garantiza una única solución.
mejor_diagnostico(Sintomas, Falla) :-
    todos_puntajes(Sintomas, Pares),
    Pares \= [],
    msort(Pares, Ordenados),
    last(Ordenados, MaxPuntaje-_),
    member(MaxPuntaje-Falla, Pares), !.


% ============================================================
% PREDICADOS AUXILIARES
% ============================================================

% Cuenta cuántos elementos de ListaRef están en ListaSintomas.
% El corte (!) evita contar el mismo síntoma más de una vez.
contar_coincidencias([], _, 0).
contar_coincidencias([S|Resto], ListaSintomas, Total) :-
    member(S, ListaSintomas), !,
    contar_coincidencias(Resto, ListaSintomas, Subtotal),
    Total is Subtotal + 1.
contar_coincidencias([_|Resto], ListaSintomas, Total) :-
    contar_coincidencias(Resto, ListaSintomas, Total).

% Verifica que todos los elementos de la lista son síntomas válidos del sistema.
todos_sintomas_validos([]).
todos_sintomas_validos([S|Resto]) :-
    sintoma(S),
    todos_sintomas_validos(Resto).

% Reúne todas las recomendaciones de una falla en una lista.
todas_recomendaciones(Falla, Lista) :-
    findall(R, recomendacion(Falla, R), Lista).

% Reúne todos los diagnósticos posibles con sus puntajes.
todos_diagnosticos(Sintomas, Lista) :-
    findall(Puntaje-Falla, puntaje_falla(Sintomas, Falla, Puntaje), Lista).

% Punto de entrada principal: valida síntomas, determina falla y reúne recomendaciones.
diagnostico_completo(Sintomas, Falla, Recomendaciones) :-
    todos_sintomas_validos(Sintomas),
    mejor_diagnostico(Sintomas, Falla),
    todas_recomendaciones(Falla, Recomendaciones).
