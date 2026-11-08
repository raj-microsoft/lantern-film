"""Original Lantern film. All shapes, character rigs and sound synthesized in code.
Run: python src/build_film.py [--4k]. Requires numpy, Pillow, ffmpeg.
"""
from pathlib import Path
import math, json, subprocess, wave, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[1]; A=ROOT/'assets'; A.mkdir(exist_ok=True)
W,H=(3840,2160) if '--4k' in sys.argv else (1920,1080)
S=W/1920; FPS=30; SR=48000; DURATION=30
INK='#233b42'; PAPER='#ecdfc6'; TEAL='#416b70'; GOLD='#f3bd61'; NIGHT='#20383f'; WHITE='#fff5df'
def font(n): return ImageFont.truetype(str(A/'Figtree.ttf'),round(n*S))
def box(d,xy,fill,r=0,outline=None,width=1):
    p=tuple(round(v*S) for v in xy)
    if r: d.rounded_rectangle(p,round(r*S),fill,outline,width=round(width*S))
    else: d.rectangle(p,fill,outline,width=round(width*S))
def ell(d,xy,fill,outline=None,width=1): d.ellipse(tuple(round(v*S) for v in xy),fill,outline,width=round(width*S))
def line(d,xy,fill,width=3): d.line([(round(x*S),round(y*S)) for x,y in xy],fill,width=round(width*S))
def text(d,xy,txt,size=32,fill=INK,anchor='lt'): d.text(tuple(round(v*S) for v in xy),txt,font=font(size),fill=fill,anchor=anchor)
def poly(d,pts,fill): d.polygon([(round(x*S),round(y*S)) for x,y in pts],fill)
def smooth(t): return (1-math.cos(math.pi*max(0,min(1,t))))/2

def lantern(d,x,y,scale,t):
    """Rig: body, hinged handle, two eye anchors, squash and breathing light."""
    s=scale; y+=math.sin(t*2)*7*s
    ell(d,(x-80*s,y+107*s,x+80*s,y+125*s),'#b6b49b')
    ell(d,(x-52*s,y-130*s,x+52*s,y-24*s),None,INK,9*s)
    box(d,(x-86*s,y-70*s,x+86*s,y+105*s),GOLD,35*s)
    box(d,(x-68*s,y-48*s,x+68*s,y+86*s),'#ffe1a0',26*s)
    box(d,(x-82*s,y+91*s,x+82*s,y+109*s),INK,7*s)
    blink=abs(math.sin(t*.8))<.035
    for dx in [-26,26]:
        if blink: line(d,[(x+dx*s-5*s,y+9*s),(x+dx*s+5*s,y+9*s)],INK,4*s)
        else: ell(d,(x+(dx-5)*s,y,x+(dx+5)*s,y+13*s),INK)
    d.arc(tuple(round(v*S) for v in (x-12*s,y+17*s,x+12*s,y+34*s)),0,180,fill=INK,width=round(3*s*S))

def person(d,x,y,s,t,color,child=False):
    """Original cut-paper human rig, rotating arms and walking feet."""
    swing=math.sin(t*3)*12*s
    skin='#c79570' if not child else '#d8ad84'
    for dx,sw in [(-17,swing),(17,-swing)]:
        line(d,[(x+dx*s,y+50*s),(x+(dx+sw*.3)*s,y+115*s)],INK,13*s)
    box(d,(x-37*s,y-31*s,x+37*s,y+64*s),color,22*s)
    line(d,[(x-28*s,y-10*s),(x-57*s,y+38*s+swing)],skin,12*s)
    line(d,[(x+28*s,y-10*s),(x+58*s,y+32*s-swing)],skin,12*s)
    ell(d,(x-27*s,y-89*s,x+27*s,y-30*s),skin)
    d.pieslice(tuple(round(v*S) for v in (x-28*s,y-95*s,x+28*s,y-40*s)),180,350,fill=INK)
    ell(d,(x+8*s,y-65*s,x+12*s,y-60*s),INK)

def room(d,t,night=False):
    box(d,(0,0,1920,1080),NIGHT if night else PAPER)
    box(d,(0,730,1920,1080),'#304b51' if night else '#c6c6a9')
    box(d,(180,150,690,600),'#527279' if night else '#96b8b2',100)
    ell(d,(430,218,535,323),'#f8df9b' if night else '#ffe4a3')
    box(d,(180,478,690,601),'#476469' if night else '#789691')
    line(d,[(435,150),(435,600)],PAPER,14)
    line(d,[(180,375),(690,375)],PAPER,14)
    # Houseplant with deliberate cut-paper leaves
    for j in range(5):
        yy=560-j*42
        line(d,[(1640,746),(1634+j*4,yy)],TEAL,8)
        ell(d,(1570,yy-15,1640,yy+24),'#709080')
        ell(d,(1630,yy-40,1700,yy),'#7a9883')
    poly(d,[(1585,680),(1695,680),(1672,770),(1608,770)],'#ad765b')

def caption(d,txt,sub=None,night=False):
    color=WHITE if night else INK
    text(d,(960,880),txt,66,color,'mt')
    if sub: text(d,(960,976),sub,25,color,'mt')

SCENES=[
(0,4,'A little light.','Meet Lantern.','Portrait; Lantern wakes on a quiet tabletop.'),
(4,9,'For the everyday.','A small AI, imagined for family life.','Wide morning room; two original characters cross the frame.'),
(9,14,'The little things, remembered.','Tomorrow: library books.','Close-up; a book reminder arrives beside Lantern.'),
(14,20,'A nudge. Never a decision.','Send a reminder? Only when you say so.','Split composition; reminder waits for a human OK.'),
(20,25,'More room for being together.','Less to carry into the evening.','Evening wide; the family gathers around the table.'),
(25,30,'Lantern','A little light for your day.','End frame; Lantern settles beside the wordmark.')]

def frame(t):
    im=Image.new('RGB',(W,H),PAPER); d=ImageDraw.Draw(im)
    idx=next(i for i,(a,b,*_) in enumerate(SCENES) if a<=t<b); a,b,cap,sub,_=SCENES[idx]; u=t-a
    if idx==0:
        room(d,t); box(d,(500,710,1420,750),INK,12)
        line(d,[(590,750),(560,830)],INK,18); line(d,[(1330,750),(1360,830)],INK,18)
        lantern(d,960,550,1.35,t)
        text(d,(960,96),'Lantern',43,INK,'mt'); caption(d,cap,sub)
    elif idx==1:
        room(d,t); box(d,(850,658,1500,695),INK,12)
        lantern(d,1340,552,.82,t)
        person(d,480+u*30,590,1.35,t,TEAL)
        person(d,725+u*34,642,.95,t,'#a87559',True)
        caption(d,cap,sub)
    elif idx==2:
        room(d,t); lantern(d,540,540,1.35,t)
        dy=35*(1-smooth(u/1.2))
        box(d,(825,270+dy,1510,690+dy),WHITE,24)
        text(d,(885,325+dy),'Tomorrow, before you go',31)
        # book stack
        box(d,(885,410+dy,1005,555+dy),TEAL,7)
        box(d,(898,410+dy,907,555+dy),'#8eaca4')
        text(d,(1040,427+dy),'Library books',40)
        text(d,(1040,491+dy),'Back in the school bag.',28)
        caption(d,cap,sub)
    elif idx==3:
        box(d,(0,0,1920,1080),'#aec3b8'); lantern(d,490,490,1.5,t)
        box(d,(825,245,1565,710),WHITE,24)
        text(d,(890,303),'A small thing for tomorrow',30)
        text(d,(890,376),'Send a reminder?',51)
        text(d,(890,454),'You choose what happens next.',29)
        active=u>3.7
        box(d,(890,545,1325,635),TEAL if active else '#d6dfd0',14)
        text(d,(1108,566),'Reminder set' if active else 'Waiting for your OK',29,WHITE if active else INK,'mt')
        if active: ell(d,(1360,563,1417,620),GOLD); line(d,[(1374,591),(1385,602),(1405,579)],INK,5)
        caption(d,cap,sub)
    elif idx==4:
        room(d,t,True)
        person(d,650,510,1.3,t*.15,'#89a79c'); person(d,1250,520,1.2,t*.15,'#b67e60'); person(d,950,600,.85,t*.2,'#d7ad64',True)
        box(d,(475,685,1445,730),'#b68b65',20)
        line(d,[(570,730),(555,815)],'#b68b65',20); line(d,[(1350,730),(1365,815)],'#b68b65',20)
        for x in (720,1180): ell(d,(x-70,680,x+70,705),PAPER)
        lantern(d,960,634,.43,t); caption(d,cap,sub,True)
    else:
        box(d,(0,0,1920,1080),NIGHT)
        lantern(d,960,400,1.22,t)
        text(d,(960,605),'Lantern',138,WHITE,'mt')
        text(d,(960,805),sub,48,WHITE,'mt')
        text(d,(960,990),'An original, fictional product film',23,'#b8cac3','mt')
    # restrained cut-to-paper dissolve at scene boundaries
    fade=max(0,1-u/.28)
    if fade>0: im=Image.blend(im,Image.new('RGB',(W,H),PAPER if idx<4 else NIGHT),fade)
    return im

def score():
    """120 BPM / 60 beats. Cmaj7–Am7–Fmaj7–Gadd9, felt-like sine partials."""
    n=SR*DURATION; audio=np.zeros((n,2),dtype=np.float64)
    def note(midi,start,dur,gain,pan=0):
        count=min(int(dur*SR),n-int(start*SR))
        if count<=0:return
        t=np.arange(count)/SR; hz=440*2**((midi-69)/12)
        env=(1-np.exp(-t*45))*np.exp(-t*1.7)*np.minimum(1,(dur-t)/.12)
        sound=(np.sin(2*np.pi*hz*t)+.24*np.sin(2*np.pi*hz*2*t)+.065*np.sin(2*np.pi*hz*3*t))*env*gain
        pos=int(start*SR); audio[pos:pos+count,0]+=sound*(.72-pan*.22); audio[pos:pos+count,1]+=sound*(.72+pan*.22)
    chords=[[48,55,59,64],[45,52,55,60],[41,48,52,57],[43,50,57,62]]
    melody=[72,76,79,76,74,72,67,71,72,76,81,79,76,74,72]
    for beat in range(60):
        chord=chords[(beat//8)%4]
        if beat%4==0:
            for k,m in enumerate(chord):note(m,beat*.5+k*.028,2.4,.065,(k-1.5)/2)
        note(chord[(beat%4)]+12,beat*.5,1.3,.055,(-1)**beat*.55)
        if beat%4==0:note(melody[beat//4],beat*.5,1.7,.1,.1)
    # stereo room echoes, deterministic; no sampled/copyrighted audio
    for delay,gain in [(.1875,.16),(.375,.1)]:
        off=int(delay*SR);audio[off:]+=audio[:-off,::-1].copy()*gain
    ramp=np.minimum(1,np.arange(n)/SR/1.5)*np.minimum(1,(n-np.arange(n))/SR/2)
    audio*=ramp[:,None]; audio*=.8/max(np.max(np.abs(audio)),1e-8)
    with wave.open(str(A/'score.wav'),'wb') as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(SR);f.writeframes((audio*32767).astype('<i2').tobytes())

def run(cmd): return subprocess.run(cmd,check=True,capture_output=True,text=True)
def main():
    score()
    suffix='-4k' if W==3840 else ''
    raw=A/('silent'+suffix+'.mp4')
    cmd=['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r','30','-i','-','-an','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p',str(raw)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for i in range(900):
        im=frame(i/30);p.stdin.write(im.tobytes())
        if i in [60,180,330,510,675,840]: im.resize((960,540)).save(A/f'shot-{i//150+1}.jpg',quality=92)
        if i==60: im.save(A/'poster.jpg',quality=94)
        if i%150==0:print(f'Frame {i}/900',flush=True)
    p.stdin.close(); assert p.wait()==0
    measured=run(['ffmpeg','-i',str(A/'score.wav'),'-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-']).stderr
    stats=json.loads(measured[measured.rfind('{'):measured.rfind('}')+1])
    filt=f"loudnorm=I=-16:TP=-1.5:LRA=11:measured_I={stats['input_i']}:measured_TP={stats['input_tp']}:measured_LRA={stats['input_lra']}:measured_thresh={stats['input_thresh']}:offset={stats['target_offset']}:linear=true:print_format=json"
    out=A/('lantern'+suffix+'.mp4')
    run(['ffmpeg','-y','-i',str(raw),'-i',str(A/'score.wav'),'-map','0:v','-map','1:a','-c:v','copy','-af',filt,'-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart','-t','30',str(out)])
    report=run(['ffmpeg','-i',str(out),'-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-']).stderr
    final=json.loads(report[report.rfind('{'):report.rfind('}')+1]); final['bytes']=out.stat().st_size
    (ROOT/'checks'/f'loudness{suffix}.json').write_text(json.dumps(final,indent=2))
    probe=run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(out)]).stdout
    (ROOT/'checks'/f'ffprobe{suffix}.json').write_text(probe)
    run(['ffmpeg','-y','-i',str(out),'-vn','-c:a','copy',str(A/'score.m4a')])
    print(json.dumps(final),flush=True)
if __name__=='__main__':main()
