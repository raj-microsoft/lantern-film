# Lantern — a little light for your day
An original 30-second animated launch-film concept for a **fictional** family AI. No real monitoring product, family data, sampled audio or purchases. Includes clearly labeled AI-generated fictional family imagery.

## Watch and inspect
- Published site: https://raj-microsoft.github.io/lantern-film/
- Entire deterministic film project: [film.html](film.html)
- Native 1080p: assets/lantern.mp4
- Native 4K: assets/lantern-4k.mp4
- Five separate audio parts: assets/stems/

## True claims before scripting
1. Lantern is an original fictional product concept, not a released AI service.
2. The film imagines a library-book reminder and shows a human approving it; it does not demonstrate a working assistant.
3. The Lantern character and surrounding world are original code drawings. Two ChatGPT-generated photoreal fictional-family plates appear in scenes 3 and 4, without personal data.
4. All music and cue effects are original synthesis; no sampled audio or voice recording is used.
All proposed capabilities are presented as part of this labeled fiction, never as product facts.

## Full guide credit
[Making the dots Film with Opus 5.5](https://achieved-cloak-445.notion.site/Making-the-dots-film-with-Opus-5-5-3f0e13e8b390813f9ac7ce05c2ec7df1), Ashok Reddy S, also listed in the [AI Web Design Library](https://raj-microsoft.github.io/ai-web-design-library/).
The site follows all 14 headings (00–13), including true claims, deterministic one-page film, posed characters, beat timing, five-part audio, real motion blur, frame QC and a native 4K master. HyperFrames is optional and not used.

## Reproduce
Python 3.12+, Node, ffmpeg on PATH, Edge installed (or set CHROME_PATH to a Chromium executable):

```text
pip install numpy pillow
npm ci
python src/build_film.py
python src/frame_qc.py
python src/build_film.py --4k
python src/frame_qc.py --4k
python src/verify.py
```

`film.html` is the complete film. `src/film.js` implements a deterministic `seek(t)`; scene/rig state never relies on previous frames. `src/render.cjs` runs it in headless Edge (Chromium). Each output frame averages four independent time samples over a 1/60-second shutter, then draws sharp captions. This is temporal supersampling, not post-process blur. 900 frames per master, 30 fps.

`src/score.py` synthesizes five parts with NumPy and wave: warm harmony, round bass, arpeggio, melody and cue effects, 48 kHz stereo / 120 BPM. Original effects are dedicated to CC0; see assets/effects-CC0.txt and checks/audio-cues.json. Two-pass loudnorm targets -16 LUFS; the encoded AAC is measured again. `input_i` in checks/loudness.json is the actual published-file measurement, not `output_i` (a hypothetical additional normalization).

## Substitutions
- Original flat Canvas characters with squash/stretch, leans, blinks and hops replace official 3D plush rigs and 64-shell fur.
- ChatGPT image generation supplies two AI-generated family stills. Gemini Veo uploads failed in both JPEG and PNG formats; deterministic Canvas push-in and light drift provide the documented motion fallback. See assets/photoreal/PROVENANCE.md.
- Captions replace ElevenLabs voice; there is deliberately no voice track.
- A quiet original 120 BPM score replaces electro-pop to honor the calm brief.
- Original CC0 synthesis replaces downloaded Kenney CC0 effects, with explicit provenance and cue sheet.
- Installed headless Edge uses the Chromium rendering engine instead of Chrome branding.
- This coding environment replaces Claude Code. No claim that Opus created this film.
- Optional HyperFrames omitted; scene functions, captions and audio stems remain separated in source.

## Checks
Published masters measure -16.01 LUFS and -1.88 dBTP; payload sizes are recorded in checks/loudness.json and checks/loudness-4k.json. The 1080p file must stay below 3 MB and native 4K below 6 MB. Live Edge checks at 1440px and 390px confirm HTTP 200, no horizontal overflow or JavaScript errors, 14 pipeline headings, five stems, working shot cues and deterministic preview. Detector: zero findings.

checks/render*.json records determinism and motion-blur checks; ffprobe*.json records native dimensions, frame count and duration; loudness*.json records final encoded levels. frame-qc*.json combines ffmpeg black/freeze scanning with MD5 comparison of every decoded adjacent frame. The -80 dB freeze threshold distinguishes quiet breathing animation from actual freezes; zero identical adjacent frames is checked separately.

## Asset provenance and access
The photoreal poster is scene 3 at 11 seconds, compositing a ChatGPT-generated family plate with original coded art. Six shot stills are Canvas output at frames 60/180/330/510/675/840. Responsive WebP family stills are 960/1600px at quality 78; source provenance and hashes are in assets/photoreal/PROVENANCE.md. Figtree by Erik Kennedy, Google Fonts repository, SIL Open Font License (assets/OFL.txt). Cue effects only are CC0-1.0; no downloaded samples.
Accessible play/pause, seek, mute and fullscreen controls sit below the video image, so they cannot cover burned-in captions. Native controls remain a no-JavaScript fallback. No autoplay, reduced-motion-compatible navigation, full written script, accessible cue controls, and a silent deterministic preview with manual playback. No trackers or external runtime dependencies.
