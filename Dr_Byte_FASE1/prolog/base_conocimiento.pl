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
