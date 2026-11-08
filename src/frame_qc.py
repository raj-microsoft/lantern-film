"""Decode every published video frame: black scan, low-noise freeze scan, adjacent MD5s."""
from pathlib import Path
import subprocess,json,sys
suffix='-4k' if '--4k' in sys.argv else '';p=Path(f'assets/lantern{suffix}.mp4')
r=subprocess.run(['ffmpeg','-hide_banner','-i',str(p),'-vf','blackdetect=d=0.03:pix_th=0.02,freezedetect=n=-80dB:d=0.5','-an','-f','null','-'],capture_output=True,text=True,check=True)
events=[x for x in r.stderr.splitlines() if 'black_start:' in x or 'freeze_start:' in x]
h=subprocess.run(['ffmpeg','-v','error','-i',str(p),'-map','0:v','-f','framemd5','-'],capture_output=True,text=True,check=True).stdout
hashes=[x.rsplit(',',1)[1].strip() for x in h.splitlines() if not x.startswith('#')]
dup=sum(a==b for a,b in zip(hashes,hashes[1:]))
result={'decodedFrames':len(hashes),'adjacentIdenticalFrames':dup,'blackDetection':'d=0.03, pix_th=0.02','freezeDetection':'noise=-80dB, duration=0.5s (quiet animated holds)','events':events,'pass':len(hashes)==900 and not events and not dup}
Path(f'checks/frame-qc{suffix}.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
assert result['pass']
