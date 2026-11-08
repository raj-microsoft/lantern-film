"""Build the browser film plus five-part Python score. python src/build_film.py [--4k]
Dependencies: numpy, Pillow; npm install; ffmpeg on PATH; Edge or CHROME_PATH.
"""
from pathlib import Path
import subprocess,sys,json
from score import build
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'assets'
def run(cmd):return subprocess.run(cmd,cwd=ROOT,check=True,capture_output=True,text=True)
def stats(log):return json.loads(log[log.rfind('{'):log.rfind('}')+1])
def main():
    four='--4k' in sys.argv;suffix='-4k' if four else '';build()
    subprocess.run(['node','src/render.cjs']+(['--4k'] if four else []),cwd=ROOT,check=True)
    s=stats(run(['ffmpeg','-i',str(A/'score.wav'),'-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-']).stderr)
    filt=f"loudnorm=I=-16:TP=-1.5:LRA=11:measured_I={s['input_i']}:measured_TP={s['input_tp']}:measured_LRA={s['input_lra']}:measured_thresh={s['input_thresh']}:offset={s['target_offset']}:linear=true:print_format=json"
    out=A/f'lantern{suffix}.mp4'
    run(['ffmpeg','-y','-i',str(A/f'silent{suffix}.mp4'),'-i',str(A/'score.wav'),'-map','0:v','-map','1:a','-c:v','copy','-af',filt,'-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart','-t','30',str(out)])
    final=stats(run(['ffmpeg','-i',str(out),'-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-']).stderr);final['bytes']=out.stat().st_size
    (ROOT/'checks'/f'loudness{suffix}.json').write_text(json.dumps(final,indent=2))
    (ROOT/'checks'/f'ffprobe{suffix}.json').write_text(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(out)]).stdout)
    if not four:
        run(['ffmpeg','-y','-i',str(out),'-vn','-c:a','copy',str(A/'score.m4a')])
        for wav in (A/'stems').glob('*.wav'):run(['ffmpeg','-y','-i',str(wav),'-c:a','aac','-b:a','128k',str(wav.with_suffix('.m4a'))])
    # Decoded frame QC, independently of generator and source canvas.
    log=run(['ffmpeg','-i',str(out),'-vf','blackdetect=d=0.03:pix_th=0.02,freezedetect=n=-80dB:d=0.5','-an','-f','null','-']).stderr
    events=[line for line in log.splitlines() if 'black_start:' in line or 'freeze_start:' in line]
    (ROOT/'checks'/f'frame-qc{suffix}.json').write_text(json.dumps({'frames':900,'blackDetection':'d=0.03, pix_th=0.02','freezeDetection':'noise=-80dB, duration=0.5s','events':events,'pass':not events},indent=2))
    print(json.dumps(final),flush=True)
if __name__=='__main__':main()
