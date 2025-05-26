import os
import shutil
import random

CONST_PATH_ROOT = "logs"
QUANTITY_TEST_FILES = 20
def crea_test_files(path_root):
    if not os.path.isdir(path_root):
        print(f"Error: El path raiz '{path_root}' no existe.")
        return

    extensions = [".log_app_1", ".log_app_2", ".log_app_3"]

    for i in range(QUANTITY_TEST_FILES):
        random_extension = random.choice(extensions)
        name_file = f"file_{i}{random_extension}"
        path_file = os.path.join(path_root, name_file)
        with open(path_file, "w") as file:
            file.write(f"Contenido del archivo {i}")
            print(f"Archivo creado: {path_file}")

def clasificar_logs(path_root):
    if not os.path.isdir(path_root):
        print(f"Error: El path raiz '{path_root}' no existe.")
        return

    folder_script = os.path.dirname(os.path.abspath(__file__))
    folder_logs = os.path.join(folder_script, "logs_clasificados")

    folder_extensions = {
        ".log_app_1": "app1_logs",
        ".log_app_2": "app2_logs",
        ".log_app_3": "app3_logs"
    }

    if not os.path.exists(folder_logs):
        try:
            os.makedirs(folder_logs)
        except OSError as e:
            print(f"Error al crear la carpeta base {folder_logs}: {e}")
            return

    for folder_extension in folder_extensions.values():
        path_folder_extension = os.path.join(folder_logs, folder_extension)
        if not os.path.exists(path_folder_extension):
            try:
                os.makedirs(path_folder_extension)
            except OSError as e:
                print(f"Error al crear la subcarpeta {path_folder_extension}: {e}")
                return

    count_moved = 0
    count_not_moved = 0
    count = 0

    print(f"\n------------ Inicia procesamiento de archivos... ------------\n")
    try:
        for name_file in os.listdir(path_root):
            count += 1
            path_file_origen = os.path.join(path_root, name_file)

            if os.path.isfile(path_file_origen):        #Si es un archivo
                moved = False
                for ext, folder_extension in folder_extensions.items():
                    if name_file.endswith(ext):
                        path_folder_extension_final = os.path.join(folder_logs, folder_extension)
                        path_file_destiny = os.path.join(path_folder_extension_final, name_file)

                        try:
                            shutil.move(path_file_origen, path_file_destiny)
                            print(f"{count}. Archivo movido: '{name_file}' -> '{path_folder_extension_final}'")
                            count_moved += 1
                            moved = True
                            break
                        except Exception as e:
                            print(f"Error al mover el archivo '{name_file}': {e}")
                if not moved:
                    print(f"{count}. Archivo no movido (no se reconoce extensión): '{name_file}'")
                    count_not_moved +=1
            else:
                print(f"{count}. No se mueve porque no es un archivo '{name_file}'")
                count_not_moved +=1
    except FileNotFoundError:
        print(f"Error: No se pudo acceder a '{path_root}'.")
        return
    except Exception as e:
        print(f"Ocurrió un error en'{path_root}': {e}")
        return


    print("\n ------------ Finaliza procesamiento de archivos ------------\n")
    print(f"Total de archivos movidos: {count_moved}")
    print(f"Archivos con problemas: {count_not_moved}")
    print(f"Logs clasificados se encuentran en: {folder_logs}")

if __name__ == "__main__":

    script_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(script_dir, CONST_PATH_ROOT)

    # print("Inicia creación de archivos de prueba...")
    # crea_test_files(path)
    # print("\nArchivos creado_s.")
    print("Iniciando script de clasificación de logs en path: ", path)
    clasificar_logs(path)
    print("\nScript finalizado.")