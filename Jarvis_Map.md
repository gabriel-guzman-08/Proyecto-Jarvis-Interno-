# JARVIS MAPA MENTAL


presets.json(se encargan de que Jarvis sea inteligente con mi set up y pueda modificar cosas de manera automática)

# jarvis.py

→ archivo principal/inicio del programa
contiene la key principal del proyecto
imprime la info, si Jarvis arrancó de manera correcta o incorrecta. 
Tiene el def Main

# main_window.py
→ interfaz principal

def resource_path(relative_path): (Busca archivos correctamente, íconos, assets, imágenes)"2" 

class JarvisMainWindow(QWidget):

def __init__(self): (Inicia toda la ventana principal, crea la ventana, define tamaños,íconos)"1"
def apply_theme(self): (Aplica todos el estilo visual, los colores, los fondos, los bordes etc)"2"
def build_ui(self):(construye TODA la interfaz, todos los paneles, listas, botones etc)"1"
def set_orb_state(self, state):(Cambia el estado visual del orbe, escuchando, hablando idle.)"2"
def set_orb_voice_level(self, level):(Actualiza la animación del orbe dependiendo del volumen)"3"
def cargar_presets_ui(self):(Carga los presets de presets.json y los muestra en la interfaz)"1"
def ejecutar_preset_desde_ui(self, item):(Cuando el usuario hace doble click ejecutar preset etc) "1"
def abrir_modal_preset(self, nombre_original=None, datos=None):(Editor de presets padres e hijos) "2"
def buscar_app():(Abre explorador de archivos para seleccionar .exe)"3"
def guardar():(guardar presets en presets.json)"1"
def closeEvent(self, event):(Cierra correctamente workers/procesos al salir.)"2"
def editar_preset(self):(Carga preset seleccionado y abre editor.)"2"
def delete_preset(self):(Elimina presets del JSON.)"2"
def add_preset_contextual(self):(Abre modal para agregar presets.)"3"

# jarvis_core.py
→ lógica/comandos

API_KEY (Conecta con OpenAI.)"1"
client = OpenAI(...) (Crea cliente para comunicarse con OpenAI.)"1"
conversation_history(Guarda memoria conversacional de Jarvis.)"1"
pygame.mixer.init(Inicializa sistema de audio.)"2"

def hablar(texto):(Convierte texto → voz usando Piper.)
def detener_habla():(Detiene audio actual si Jarvis está hablando.)"2"
def resetear_conversacion():(Borra historial conversacional. Mantiene solo prompt system.)"2"
def cargar_presets():(carga los presets.json)"1"

def procesar_comando(texto):(interpreta comandos, literalmente es el cerebro principal de Jarvis)"0"
PARTES INTERNAS IMPORTANTES de procesar_comando()
texto = texto.lower().strip()(Normaliza texto.)
presets = cargar_presets()(Trae automatizaciones.)
todos_presets = [](Lista temporal de presets.)
for nombre_preset, config in presets.items():(recorre todos los presets)
if "audio_device" in config:(Cambia dispositivo audio.)
for url in config.get("urls", []):()(Abre las URLS)
for app in config.get("apps", []):(Abre programas/juegos.)
client.chat.completions.create()(Manda conversación a OpenAI.)

# jarvis_worker.py
→ voz/procesos

QThread(hacer tareas sin congelar la interfaz)"1"
Signal(enviar mensajes/eventos a la interfaz)"1"
speech_recognition as sr(Reconocimiento de voz.)"1"
traceback(Mostrar errores detallados.)"2"
threading(Herramientas de threading/procesos paralelos.)"2"
hablar, procesar_comando, detener_habla(conecta worcer con IA, voz, automatización)"1"

class JarvisWorker(QThread):(proceso que escucha constantemente)"1"
state_changed = Signal(str)(comunicación worker → UI)"1"

def __init__(self):(Inicializa worker.)"1"
self.running = True(Controla loop principal.)"1"

def run(self):(probablemente el segundo def más importante de TODO Jarvis después de procesar_comando. MANTIENE VIVO A JARVIS)"0"
r = sr.Recognizer()(Crea motor reconocimiento voz.)"1"
with sr.Microphone() as source:(Accede al micrófono.)"1"
while self.running:(Loop infinito principal.)"1"
self.state_changed.emit("listening")(Le dice a la interfaz Jarvis está escuchando)"1"
audio = r.listen(...)(captura el audio del mic)"1"
texto = r.recognize_google(...)(convierte la voz en texto)"1"
if "jarvis" not in texto_lower:(Ignorar todo si no dije Jarvis)"1"
comando = texto_lower.replace("jarvis", "").strip()(Extrae comando limpio, pregunta al cerebro que hacer.)"1"
hablar(respuesta)(Jarvis responde con voz.)"1"
except sr.UnknownValueError:(Ignora audio no entendido.)"2"
traceback.print_exc()(Muestra errores completos en la terminal.)"1"
self.running = False(Eso apaga el loop principal cuando se cierra a Jarvis.)"1"

