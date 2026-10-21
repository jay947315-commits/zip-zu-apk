# ZIP zu APK

Dieses Repository verwendet GitHub Actions als Build-Server, um ein Android-
Studio-/Gradle-Projekt aus einer ZIP-Datei zu einer Debug-APK zu bauen.

## APK bauen

1. Lege die ZIP-Datei des Android-Projekts unter `input/app.zip` ab und lade
   sie in dieses Repository hoch. Das Archiv muss ein Android-Projekt mit
   `gradlew` (Gradle Wrapper) enthalten.
2. Der Build startet automatisch, sobald eine ZIP-Datei unter `input/`
   geändert wird. Alternativ kannst du unter **Actions → Build APK from
   Android ZIP → Run workflow** einen Build starten und den ZIP-Pfad angeben.
3. Öffne den abgeschlossenen Workflow-Lauf und lade unter **Artifacts** das
   Artefakt `android-debug-apk` herunter. Darin liegt die APK.

Es wird eine **Debug-APK** gebaut, die zum Testen und Installieren gedacht
ist. Für eine veröffentlichungsfähige Release-APK sind ein Release-Build und
eine eigene Signierung nötig.

## Voraussetzungen und Sicherheit

- Die ZIP muss ein baubares Android-Projekt mit Gradle Wrapper (`gradlew`)
  enthalten. Beliebige ZIP-Dateien oder bereits gebaute APKs werden nicht
  konvertiert.
- Das ZIP-Archiv wird auf sichere Pfade und symbolische Links geprüft, bevor
  es entpackt wird.
- Der Build führt Gradle-Buildskripte aus dem Projekt aus. Verwende daher nur
  ZIP-Dateien aus vertrauenswürdigen Quellen. Der Workflow erhält keine
  Repository-Schreibberechtigungen oder Secrets.