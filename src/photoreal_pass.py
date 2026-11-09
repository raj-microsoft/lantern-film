"""One-time photoreal scene and documentation upgrade."""
from pathlib import Path
p=Path('src/film.js');s=p.read_text(encoding='utf-8')
if 'function lifeCard(' in s:
    raise SystemExit('Photoreal migration already applied; use build_film.py to re-render.')
s=s.replace("let c=sampleCtx;", """let c=sampleCtx;
// AI-generated still plates. Deterministic restrained push-in is the documented
// fallback after Gemini's image uploads failed; no invented Veo footage.
const plates={};
const platesReady=Promise.all(['evening','morning'].map(name=>new Promise((resolve,reject)=>{
 const image=new Image();image.onload=()=>{plates[name]=image;resolve();};image.onerror=reject;
 image.src=`assets/photoreal/${name}-1600.webp`;
})));
function lifeCard(name,x,y,w,h,u,duration){
 rect(x-12,y-12,w+24,h+24,P.white,24);
 c.save();c.beginPath();c.roundRect(x,y,w,h,16);c.clip();
 const image=plates[name],progress=clamp(u/duration),zoom=1+.025*progress;
 const scale=Math.max(w/image.width,h/image.height)*zoom;
 const dw=image.width*scale,dh=image.height*scale;
 c.drawImage(image,x+(w-dw)/2,y+(h-dh)/2,dw,dh);
 // A barely perceptible warm light drift; all animation derives only from t.
 c.fillStyle=`rgba(255,215,155,${.012+.009*Math.sin(progress*Math.PI)})`;
 c.fillRect(x,y,w,h);c.restore();
 text(x,y-55,name==='evening'?'An evening, together.':'A morning, on your terms.',27);
 text(x,y+h+29,'AI-generated family · an imagined day',21);
}
""")
a=s.index(" {start:9,end:14,");b=s.index(" {start:20,end:25,",a)
s=s[:a]+""" {start:9,end:14,caption:'The little things, remembered.',line:'Tomorrow: library books.',draw(t,u){room(t);
 const dy=35*(1-spring(u/.5));lifeCard('evening',150,260+dy,790,444,u,5);
 lantern(1410,370,.86,t,{hop:5,lean:-.03});rect(1080,535,650,190,P.white,22);
 rect(1115,577,70,95,P.teal,5);rect(1123,577,6,95,'#8eaca4');
 text(1220,566,'Tomorrow: library books',31);text(1220,623,'Back in the school bag.',26);}},
 {start:14,end:20,caption:'A nudge. Never a decision.',line:'Send a reminder? Only when you say so.',draw(t,u){rect(0,0,1920,1080,'#aec3b8');
 lifeCard('morning',150,260,790,444,u,6);lantern(1410,310,.69,t,{hop:4,lean:.025});
 rect(1065,435,690,300,P.white,24);text(1110,474,'Send a reminder?',43);
 text(1110,539,'You choose what happens next.',26);const yes=u>=4;
 rect(1110,599,470,80,yes?P.teal:'#d6dfd0',14);text(1345,621,yes?'Reminder set':'Waiting for your OK',27,yes?P.white:P.ink,'center');
 if(u>=3){const q=ease((u-3)/1),cx=1720-260*q,cy=770-130*q;poly([[cx,cy],[cx+6,30+cy],[cx+15,21+cy],[cx+29,20+cy]],P.ink);}
 if(yes){ellipse(1660,639,27,27,P.gold);line([[1646,639],[1657,650],[1677,627]],P.ink,5);}}},
"""+s[b:]
s=s.replace("window.filmReady=document.fonts.load('400 66px Figtree').then", "window.filmReady=Promise.all([document.fonts.load('400 66px Figtree'),platesReady]).then")
p.write_text(s,encoding='utf-8')
p=Path('src/render.cjs');s=p.read_text();s=s.replace("four?'22':'20'","four?'26':'24'");p.write_text(s)
p=Path('src/verify.py');s=p.read_text(encoding='utf-8');s=s.replace("<25_000_000","<(6_000_000 if suffix else 3_000_000)").replace('each <25MB','1080p <3MB / 4K <6MB');p.write_text(s,encoding='utf-8')
p=Path('index.html');s=p.read_text(encoding='utf-8')
s=s.replace('see how every frame and note was made in code.','see how coded animation meets AI-generated family imagery.')
s=s.replace('poster="assets/poster.jpg"','poster="assets/photoreal/poster-1600.webp"')
s=s.replace('Every character and scene is synthetic, made entirely in code without real family footage or personal data.','The characters are drawn in code. The fictional family images are AI-generated with ChatGPT; no real family footage or personal data is used.')
s=s.replace('Every person, room and product character is synthetic and drawn in code, with no family data.','The family is fictional: ChatGPT-generated imagery appears inside coded scenes. The Lantern character and surrounding world remain original code drawings, with no real family data.')
s=s.replace('Higgsfield is a paid service, so original coded morning and evening rooms replace live-action footage. These synthetic 2D plates are drawn in the same scene functions as the rigs, with no downloaded video or real people.','Two AI-generated photoreal stills were made with ChatGPT image generation: a quiet Dutch-home evening and the following morning. They appear in the small her-life card in scenes 3 and 4; everything around it remains drawn in code. Gemini Veo was attempted, but both JPEG and PNG uploads failed, leaving generation unavailable. The honest fallback is a restrained, deterministic Canvas push-in and warm light drift, not claimed live-action or Veo footage.')
s=s.replace('The workflow uses local tools without paid services, API keys or new accounts.','ChatGPT image generation supplies two fictional family stills through the authorized existing session; local tools handle animation and encoding. No purchases, API keys or new accounts.')
s=s.replace('Six scenes move from morning to evening.','Six scenes frame a family day, including an evening and next-morning vignette.')
s=s.replace('Lantern beside a reminder to pack library books','Coded Lantern beside an AI-generated evening family reading card and library-book reminder')
s=s.replace('A reminder awaiting human approval','AI-generated morning family card beside a coded reminder awaiting human approval')
marker='<div class="folio"><section id="shots"'
feature='''<div class="folio"><section class="section life-stills" aria-labelledby="life-title"><div class="section-heading"><h2 id="life-title">A little of her world.</h2><p>An evening with a book. A morning with room to choose. Two AI-generated moments of a fictional family, held inside the film’s coded world.</p></div><div class="life-grid"><figure><img src="assets/photoreal/evening-960.webp" srcset="assets/photoreal/evening-960.webp 960w, assets/photoreal/evening-1600.webp 1600w" sizes="(max-width: 700px) calc(100vw - 40px), 50vw" width="1600" height="900" loading="lazy" alt="AI-generated fictional family reading together at an oak table in a warm Dutch home at dusk"><figcaption>Scene 03 · Evening together · AI-generated</figcaption></figure><figure><img src="assets/photoreal/morning-960.webp" srcset="assets/photoreal/morning-960.webp 960w, assets/photoreal/morning-1600.webp 1600w" sizes="(max-width: 700px) calc(100vw - 40px), 50vw" width="1600" height="900" loading="lazy" alt="AI-generated mother beside a phone while her child packs blank library books into a teal school bag in morning light"><figcaption>Scene 04 · A morning on your terms · AI-generated</figcaption></figure></div><p class="still-note">Still by default, including with reduced motion. The film only moves when you press play.</p></section><section id="shots"'''
assert marker in s;s=s.replace(marker,feature)
p.write_text(s,encoding='utf-8')
p=Path('style.css');s=p.read_text();s+='\n.life-grid{display:grid;grid-template-columns:1fr 1fr;gap:26px}.life-grid figure{margin:0}.life-grid img{display:block;width:100%;height:auto;aspect-ratio:16/9;object-fit:cover}.life-grid figcaption,.still-note{font-size:14px;color:#425b57;margin-top:14px}.still-note{margin-top:24px}@media(max-width:700px){.life-grid{grid-template-columns:1fr;gap:30px}}\n';p.write_text(s)
