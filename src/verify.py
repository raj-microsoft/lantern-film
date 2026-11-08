from pathlib import Path
from html.parser import HTMLParser
import json
class Links(HTMLParser):
    def handle_starttag(self,tag,attrs):
        for k,v in attrs:
            if k in ['src','href'] and not v.startswith(('https:','#')):
                assert Path(v).exists(),v
Links().feed(Path('index.html').read_text(encoding='utf-8'))
probe=json.loads(Path('checks/ffprobe.json').read_text()); v=probe['streams'][0]
assert (v['width'],v['height'],v['nb_frames'],v['r_frame_rate'])==(1920,1080,'900','30/1')
assert float(probe['format']['duration'])==30
assert Path('assets/lantern.mp4').stat().st_size<25_000_000
loud=json.loads(Path('checks/loudness.json').read_text())
assert abs(float(loud['input_i'])+16)<.3
print('PASS: local assets, 1080p, 900 frames, 30 fps, 30 seconds, <25MB, -16 LUFS')
