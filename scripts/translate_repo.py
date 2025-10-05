import os
import translators as ts
from pathlib import Path

def translate_file_content(file_path, target_language='sv'):
    """
    Läser innehållet i en fil, översätter det från engelska till svenska
    och skriver över filen med det översatta innehållet.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        if not content.strip():
            print(f"Skippar tom fil: {file_path}")
            return

        translated_content = ts.translate_text(content, from_language='en', to_language=target_language)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(translated_content)

        print(f"Översatte filen: {file_path}")

    except UnicodeDecodeError:
        print(f"Kunde inte läsa filen (troligen binär): {file_path}")
    except Exception as e:
        print(f"Ett fel uppstod med filen {file_path}: {e}")

def translate_directory(directory_path, target_language='sv'):
    """
    Går igenom alla filer i en mapp och dess undermappar och översätter dem.
    """
    # Lista över filer/mappar att ignorera
    ignore_list = ['.git', '.github', 'scripts']

    for root, dirs, files in os.walk(directory_path, topdown=True):
        # Ta bort ignorerade mappar från genomgången
        dirs[:] = [d for d in dirs if d not in ignore_list]
        for filename in files:
            # Hoppa över alla filer i ignore_list (även om de inte är mappar)
            if filename in ignore_list:
                continue

            file_path = Path(root) / filename
            translate_file_content(str(file_path), target_language)

if __name__ == "__main__":
    # Bestäm rotmappen för repot (en nivå upp från där skriptet ligger)
    repo_path = os.path.join(os.path.dirname(__file__), '..')
    
    print(f"Startar översättning för mappen: {os.path.abspath(repo_path)}")
    translate_directory(repo_path)
    print("\nÖversättningen är klar!")
