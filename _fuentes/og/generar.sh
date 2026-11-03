#!/usr/bin/env bash
# Genera las imágenes de vista previa de Dos Décimas (lo que se ve al compartir el enlace en WhatsApp o Instagram).
# Uso: bash _fuentes/og/generar.sh   (necesita Google Chrome)
set -euo pipefail
cd "$(dirname "$0")"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
hacer() { # hacer <archivo> <título> <pie>
  sed -e "s|__TITULO__|$2|" -e "s|__PIE__|$3|" plantilla.html > _tmp.html
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 --window-size=1200,630 \
    --screenshot="$PWD/_tmp.png" "file://$PWD/_tmp.html" >/dev/null 2>&1
  sips -s format jpeg -s formatOptions 85 _tmp.png --out "../../img/$1" >/dev/null
  rm -f _tmp.html _tmp.png; echo "escrito img/$1"
}
hacer dosdecimas-og.jpg 'Me quedé fuera por <mark>dos décimas</mark>.<br>Que a ti no te pase.' 'Pruébala 7 días gratis'
hacer dosdecimas-test-og.jpg '¿Llegarías al <mark>7,05</mark>?' '20 preguntas reales del examen de 2026 · Gratis'
