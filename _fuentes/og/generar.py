# Genera las imágenes de vista previa (lo que se ve al compartir el enlace en WhatsApp o Instagram), con el panel de tablillas.
# Uso: python3 _fuentes/og/generar.py   (necesita Google Chrome)
import pathlib, subprocess, html
AQUI = pathlib.Path(__file__).resolve().parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PLANTILLA = (AQUI / "plantilla.html").read_text(encoding="utf-8")

def hacer(archivo, marca, filas, pie):
    """filas: [(texto de hasta 16 caracteres, "crema" | "cobre"), ...]"""
    logo, nombre = (("dosdecimas-logo.png", "Dos Décimas · Policía Nacional") if marca == "dd" else ("ruvi-monograma.png", "Ruvï"))
    panel = "".join(f'<div class="fila{" cobre" if c == "cobre" else ""}">' + "".join(f"<span>{html.escape(ch) if ch != ' ' else '&nbsp;'}</span>" for ch in t.ljust(16)[:16]) + "</div>" for t, c in filas)
    pagina = PLANTILLA.replace("__LOGO__", logo).replace("__NOMBRE__", nombre).replace("__PANEL__", panel).replace("__PIE__", pie)
    tmp, png = AQUI / "_tmp.html", AQUI / "_tmp.png"
    tmp.write_text(pagina, encoding="utf-8")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1", "--window-size=1200,630",
                    f"--screenshot={png}", tmp.as_uri()], check=True, capture_output=True)
    subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "85", str(png), "--out", str(AQUI.parent.parent / "img" / archivo)], check=True, capture_output=True)
    tmp.unlink(); png.unlink(); print("escrito img/" + archivo)

hacer("dosdecimas-og.jpg", "dd", [("ME QUEDÉ FUERA", "crema"), ("POR DOS DÉCIMAS.", "crema"), ("TE FALTAN   0,20", "cobre")], "Pruébala 7 días gratis")
hacer("dosdecimas-test-og.jpg", "dd", [("¿LLEGARÍAS", "crema"), ("AL 7,05?", "cobre")], "20 preguntas reales del examen de 2026 · Gratis")
hacer("ruvi-og.jpg", "ruvi", [("HERRAMIENTAS", "crema"), ("PARA PREPARAR", "crema"), ("OPOSICIONES.", "cobre")], "Plantilla de Repaso · Dos Décimas")
hacer("plantilla-og.jpg", "ruvi", [("TU TEMARIO", "crema"), ("CONVERTIDO EN", "crema"), ("EXAMEN.", "cobre")], "Plantilla de Repaso · Para academias · Primer mes gratis")
