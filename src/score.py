"""Original five-part score, 120 BPM. All effects are original synthesis dedicated to CC0.
Parts: warm harmony, round bass, arpeggio, melody, cue effects. Captions replace voice.
"""
from pathlib import Path
import numpy as np
import wave, json
ROOT=Path(__file__).resolve().parents[1]; A=ROOT/'assets'; SR=48000; N=30*SR
CUES=[(0,'wake'),(.5,'land'),(4,'morning'),(8,'arrival'),(9,'reminder'),(9.5,'card lands'),(14,'permission'),(17,'pointer'),(18,'approve'),(20,'evening'),(25,'wordmark'),(25.5,'final landing')]
def save(path,a):
    with wave.open(str(path),'wb') as f:
        f.setnchannels(2);f.setsampwidth(2);f.setframerate(SR);f.writeframes((np.clip(a,-1,1)*32767).astype('<i2').tobytes())
def build():
    stems={name:np.zeros((N,2),dtype=np.float64) for name in ['harmony','bass','arpeggio','melody','cue-effects']}
    def note(part,midi,start,dur,gain,pan=0):
        n=min(int(dur*SR),N-int(start*SR));t=np.arange(n)/SR;f=440*2**((midi-69)/12)
        env=(1-np.exp(-t*45))*np.exp(-t*(1.2 if part=='bass' else 1.7))*np.clip((dur-t)/.12,0,1)
        sound=(np.sin(2*np.pi*f*t)+.24*np.sin(2*np.pi*2*f*t)+.065*np.sin(2*np.pi*3*f*t))*env*gain
        pos=int(start*SR);stems[part][pos:pos+n,0]+=sound*(.72-pan*.22);stems[part][pos:pos+n,1]+=sound*(.72+pan*.22)
    chords=[[48,55,59,64],[45,52,55,60],[41,48,52,57],[43,50,57,62]]
    melody=[72,76,79,76,74,72,67,71,72,76,81,79,76,74,72]
    for beat in range(60):
        chord=chords[(beat//8)%4]
        if beat%4==0:
            for k,m in enumerate(chord):note('harmony',m,beat*.5+k*.028,2.4,.048,(k-1.5)/2)
            note('melody',melody[beat//4],beat*.5,1.7,.1,.1)
        if beat%2==0:note('bass',chord[0]-12,beat*.5,1.4,.07,-.1)
        note('arpeggio',chord[beat%4]+12,beat*.5,1.3,.055,(-1)**beat*.55)
    # No downloaded samples: repeatable bell, soft wooden click and air cue designs.
    rng=np.random.default_rng(20261109)
    for j,(start,label) in enumerate(CUES):
        dur=.45;n=min(int(dur*SR),N-int(start*SR));t=np.arange(n)/SR
        if label in ['approve','wordmark','reminder']:
            s=.07*(np.sin(2*np.pi*880*t)+.4*np.sin(2*np.pi*1320*t))*np.exp(-t*11)*(1-np.exp(-t*150))
        elif 'land' in label or label=='arrival':
            s=.055*np.sin(2*np.pi*(180*t-60*t*t))*np.exp(-t*24)*(1-np.exp(-t*150))
        else:
            noise=rng.normal(size=n);smooth=np.convolve(noise,np.ones(12)/12,mode='same')
            s=.045*smooth*np.sin(np.pi*t/dur)**2+.02*np.sin(2*np.pi*440*t)*np.exp(-t*13)
        pos=int(start*SR);stems['cue-effects'][pos:pos+n]+=s[:,None]*np.array([.85,1.0])
    for name in ['harmony','arpeggio','melody']:
        a=stems[name]
        for delay,gain in [(.1875,.16),(.375,.1)]:
            off=int(delay*SR);a[off:]+=a[:-off,::-1].copy()*gain
    ramp=np.minimum(1,np.arange(N)/SR/1.5)*np.minimum(1,(N-np.arange(N))/SR/2)
    for name in stems:stems[name]*=ramp[:,None]
    mix=sum(stems.values());gain=.78/max(np.max(np.abs(mix)),1e-8)
    (A/'stems').mkdir(exist_ok=True)
    for name,a in stems.items():save(A/'stems'/f'{name}.wav',a*gain)
    save(A/'score.wav',mix*gain)
    (ROOT/'checks'/'audio-cues.json').write_text(json.dumps({'bpm':120,'sample_rate':SR,'parts':list(stems),'voice':'Omitted; captions substitute','effects_license':'CC0-1.0, original synthesis','cues':[{'time':t,'name':n} for t,n in CUES]},indent=2))
if __name__=='__main__':build()
