from pathlib import Path
from html.parser import HTMLParser
import json
class Links(HTMLParser):
    def handle_starttag(self,tag,attrs):
        for k,v in attrs:
            if k in ['src','href'] and not v.startswith(('https:','#')):
                assert Path(v).exists(),v
html=Path('index.html').read_text(encoding='utf-8');Links().feed(html);Links().feed(Path('film.html').read_text())
for i in range(14):assert f'<h3>{i:02} ·' in html,f'Missing guide step {i}'
for suffix,size in [('',(1920,1080)),('-4k',(3840,2160))]:
    probe=json.loads(Path(f'checks/ffprobe{suffix}.json').read_text());v=probe['streams'][0]
    assert (v['width'],v['height'])==size
    assert (v['nb_frames'],v['r_frame_rate'])==('900','30/1')
    assert float(probe['format']['duration'])==30
    assert Path(f'assets/lantern{suffix}.mp4').stat().st_size<(6_000_000 if suffix else 3_000_000)
    loud=json.loads(Path(f'checks/loudness{suffix}.json').read_text());assert abs(float(loud['input_i'])+16)<.3
    qc=json.loads(Path(f'checks/frame-qc{suffix}.json').read_text());assert qc['pass']
    render=json.loads(Path(f'checks/render{suffix}.json').read_text());assert render['deterministic'] and render['motionBlurChangesPixels']
assert len(list(Path('assets/stems').glob('*.m4a')))==5
print('PASS: all local links, 14 headings, native 1080p + 4K, 900 frames each, 30 fps, 30 seconds, 1080p <3MB / 4K <6MB, -16 LUFS, no black/frozen frames, 5 stems, deterministic temporal blur')
