'use strict';
// One web page, one pure time coordinate. No randomness, wall-clock state or simulation history.
const canvas=document.getElementById('film-canvas');
const ctx=canvas.getContext('2d',{alpha:false});
const sample=document.createElement('canvas'), sampleCtx=sample.getContext('2d',{alpha:false});
const P={ink:'#233b42',paper:'#ecdfc6',teal:'#416b70',gold:'#f3bd61',night:'#20383f',white:'#fff5df'};
let c=sampleCtx;
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

const clamp=x=>Math.max(0,Math.min(1,x));
const ease=x=>{x=clamp(x);return 1-(1-x)**3;};
// Critically damped arrivals finish exactly on the next 120 BPM beat.
const spring=x=>{x=clamp(x);return x===1?1:1-Math.exp(-7*x)*Math.cos(10*x);};
function rect(x,y,w,h,fill,r=0){c.beginPath();c.roundRect(x,y,w,h,r);c.fillStyle=fill;c.fill();}
function ellipse(x,y,rx,ry,fill,stroke=null,width=1){c.beginPath();c.ellipse(x,y,Math.max(.01,rx),Math.max(.01,ry),0,0,Math.PI*2);if(fill){c.fillStyle=fill;c.fill();}if(stroke){c.lineWidth=width;c.strokeStyle=stroke;c.stroke();}}
function line(pts,color=P.ink,width=3){c.beginPath();pts.forEach(([x,y],i)=>i?c.lineTo(x,y):c.moveTo(x,y));c.lineWidth=width;c.strokeStyle=color;c.lineCap='round';c.lineJoin='round';c.stroke();}
function poly(pts,color){c.beginPath();pts.forEach(([x,y],i)=>i?c.lineTo(x,y):c.moveTo(x,y));c.closePath();c.fillStyle=color;c.fill();}
function text(x,y,s,size=32,color=P.ink,align='left',weight=400){c.font=`${weight} ${size}px Figtree`;c.textBaseline='top';c.textAlign=align;c.fillStyle=color;c.fillText(s,x,y);}
function lantern(x,y,s,t,{hop=0,lean=0,arrive=1}={}){
  const beat=(t%0.5)/0.5; const height=Math.sin(Math.PI*beat)*hop;
  // Squash on landing, stretch in flight, with independent blink and handle bones.
  const squash=.025*Math.cos(2*Math.PI*beat)*(hop?1:.22);
  ellipse(x,y+116*s,80*s*(1-height/300),8*s,'#afb39c');
  c.save();c.translate(x,y-height*s);c.rotate(lean+Math.sin(t*Math.PI)*.009);c.scale(s*(1+squash)*arrive,s*(1-squash)*arrive);
  ellipse(0,-77,52,53,null,P.ink,9);
  rect(-86,-70,172,175,P.gold,35);rect(-68,-48,136,134,'#ffe1a0',26);rect(-82,91,164,18,P.ink,7);
  const blink=(t%3.5)>.10&&(t%3.5)<.22;
  [-26,26].forEach(dx=>blink?line([[dx-5,9],[dx+5,9]],P.ink,4):ellipse(dx,6.5,5,6.5,P.ink));
  c.beginPath();c.ellipse(0,20,12,12,0,0,Math.PI);c.strokeStyle=P.ink;c.lineWidth=3;c.stroke();
  c.restore();
}
function person(x,y,s,t,color,child=false,walk=false){
  const beat=t*Math.PI*4,bob=walk?Math.abs(Math.sin(beat))*6:Math.sin(t*Math.PI)*2;
  c.save();c.translate(x,y-bob);c.scale(s,s);c.rotate(Math.sin(beat)*.008);
  const swing=walk?Math.sin(beat)*13:Math.sin(t*Math.PI)*3,skin=child?'#d8ad84':'#c79570';
  line([[-17,50],[-17+swing*.4,115]],P.ink,13);line([[17,50],[17-swing*.4,115]],P.ink,13);
  rect(-37,-31,74,95,color,22);line([[-28,-10],[-57,38+swing]],skin,12);line([[28,-10],[58,32-swing]],skin,12);
  ellipse(0,-59.5,27,29.5,skin);c.beginPath();c.ellipse(0,-68,28,27,0,Math.PI,Math.PI*2);c.fillStyle=P.ink;c.fill();
  ellipse(10,-62,2,2.5,P.ink);c.restore();
}
function room(t,night=false){
  rect(0,0,1920,1080,night?P.night:P.paper);rect(0,730,1920,350,night?'#304b51':'#c6c6a9');
  rect(180,150,510,450,night?'#527279':'#96b8b2',100);ellipse(482.5,270.5,52.5,52.5,night?'#f8df9b':'#ffe4a3');
  rect(180,478,510,123,night?'#476469':'#789691');line([[435,150],[435,600]],P.paper,14);line([[180,375],[690,375]],P.paper,14);
  for(let j=0;j<5;j++){const yy=560-j*42, sway=Math.sin(t*Math.PI*.5+j*.3)*3;line([[1640,746],[1634+j*4+sway,yy]],P.teal,8);ellipse(1605+sway,yy+4.5,35,19.5,'#709080');ellipse(1665+sway,yy-20,35,20,'#7a9883');}
  poly([[1585,680],[1695,680],[1672,770],[1608,770]],'#ad765b');
}
const scenes=[
 {start:0,end:4,caption:'A little light.',line:'Meet Lantern.',draw(t,u){room(t);rect(500,710,920,40,P.ink,12);line([[590,750],[560,830]],P.ink,18);line([[1330,750],[1360,830]],P.ink,18);lantern(960,550,1.35,t,{hop:8,arrive:.8+.2*spring(u/.5)});text(960,96,'Lantern',43,P.ink,'center');}},
 {start:4,end:9,caption:'For the everyday.',line:'A small AI, imagined for family life.',draw(t,u){room(t);rect(850,658,650,37,P.ink,12);lantern(1340,552,.82,t,{hop:4});const move=200*ease(u/4);person(480+move,590,1.35,t,P.teal,false,true);person(725+move,642,.95,t,'#a87559',true,true);}},
 {start:9,end:14,caption:'The little things, remembered.',line:'Tomorrow: library books.',draw(t,u){room(t);
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
 {start:20,end:25,caption:'More room for being together.',line:'Less to carry into the evening.',draw(t,u){room(t,true);person(650,510,1.3,t,'#89a79c');person(1250,520,1.2,t,'#b67e60');person(950,600,.85,t,'#d7ad64',true);rect(475,685,970,45,'#b68b65',20);line([[570,730],[555,815]],'#b68b65',20);line([[1350,730],[1365,815]],'#b68b65',20);[720,1180].forEach(x=>ellipse(x,692.5,70,12.5,P.paper));lantern(960,634,.43,t,{hop:3});}},
 {start:25,end:30,caption:'Lantern',line:'A little light for your day.',draw(t,u){rect(0,0,1920,1080,P.night);lantern(960,400,1.22,t,{hop:12,arrive:.9+.1*spring(u/.5)});}}
];
function sceneAt(t){return scenes.find(s=>t>=s.start&&t<s.end)||scenes[5];}
function world(t){const s=sceneAt(t);s.draw(t,t-s.start);}
function titles(t){const s=sceneAt(t),night=t>=20;const color=night?P.white:P.ink;
 if(t<25){text(960,846,s.caption,66,color,'center');text(960,940,s.line,29,color,'center');}
 else {text(960,605,'Lantern',138,P.white,'center');text(960,805,s.line,48,P.white,'center');text(960,970,'An original, fictional product film',23,'#b8cac3','center');}
}
window.configureFilm=(width=1920,height=1080)=>{canvas.width=sample.width=width;canvas.height=sample.height=height;};
// 180-degree shutter: average four independent exposure samples over 1/60 s.
// Averaging world pixels is true temporal motion blur, not CSS blur or a trailing-frame trick.
window.seek=(time,samples=4)=>{const t=Math.max(0,Math.min(29.966667,Number(time))),s=sceneAt(t),scale=canvas.width/1920;
 ctx.setTransform(1,0,0,1,0,0);ctx.globalAlpha=1;
 for(let k=0;k<samples;k++){
   const delta=samples===1?0:((k+.5)/samples-.5)/60;
   let st=Math.max(s.start,Math.min(s.end-.000001,t+delta));
   // UI approval is an instantaneous cut, not moving geometry: do not blend its two labels.
   if(s===scenes[3])st=t>=18?Math.max(18,st):Math.min(17.999999,st);
   c=sampleCtx;c.setTransform(scale,0,0,scale,0,0);c.globalAlpha=1;world(st);
   ctx.globalAlpha=1/(k+1);ctx.drawImage(sample,0,0);
 }
 ctx.globalAlpha=1;c=ctx;c.setTransform(scale,0,0,scale,0,0);titles(t);ctx.setTransform(1,0,0,1,0,0);
 return {time:t,scene:scenes.indexOf(s),samples};
};
let playing=false,start=0,base=2,raf=0;
const slider=document.getElementById('time'),toggle=document.getElementById('toggle'),readout=document.getElementById('readout');
function show(t){window.seek(t);slider.value=t;readout.textContent=t.toFixed(2)+' s';}
function stop(){playing=false;cancelAnimationFrame(raf);toggle.textContent='Play preview';}
function tick(now){const t=base+(now-start)/1000;if(t>=30){stop();show(29.966667);return;}show(t);raf=requestAnimationFrame(tick);}
toggle.onclick=()=>{if(playing){stop();return;}base=Number(slider.value);if(base>29.9)base=0;start=performance.now();playing=true;toggle.textContent='Pause preview';raf=requestAnimationFrame(tick);};slider.oninput=()=>{stop();show(Math.round(Number(slider.value)*30)/30);};
if(new URLSearchParams(location.search).has('render'))document.body.classList.add('render');
window.filmReady=Promise.all([document.fonts.load('400 66px Figtree'),platesReady]).then(()=>{window.configureFilm();show(2);return true;});
