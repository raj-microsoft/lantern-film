const player=document.getElementById('player');
const controls=document.getElementById('film-controls'),play=document.getElementById('film-play'),seek=document.getElementById('film-seek'),time=document.getElementById('film-time'),mute=document.getElementById('film-mute'),full=document.getElementById('film-fullscreen'),frame=document.getElementById('film-frame'),status=document.getElementById('playback-status');
const clock=t=>`${Math.floor(t/60)}:${String(Math.floor(t%60)).padStart(2,'0')}`;
function sync(){const duration=Number.isFinite(player.duration)?player.duration:30;seek.max=duration;seek.value=player.currentTime;seek.setAttribute('aria-valuetext',`${clock(player.currentTime)} of ${clock(duration)}`);time.textContent=`${clock(player.currentTime)} / ${clock(duration)}`;play.textContent=player.paused?(player.ended?'Replay':'Play'):'Pause';mute.textContent=player.muted?'Unmute':'Mute';mute.setAttribute('aria-pressed',String(player.muted));mute.setAttribute('aria-label',player.muted?'Unmute sound':'Mute sound');}
play.addEventListener('click',async()=>{if(!player.paused){player.pause();return;}try{if(player.ended)player.currentTime=0;await player.play();status.textContent='';}catch{status.textContent='Playback could not start. Try Play again or download the film below.';}});
seek.addEventListener('input',()=>{player.currentTime=Number(seek.value);sync();});
mute.addEventListener('click',()=>{player.muted=!player.muted;sync();});
full.addEventListener('click',async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await frame.requestFullscreen();}catch{status.textContent='Full screen is unavailable in this browser. You can download the film below.';}});
if(!frame.requestFullscreen)full.hidden=true;
document.addEventListener('fullscreenchange',()=>{full.textContent=document.fullscreenElement?'Exit full screen':'Full screen';});
for(const event of ['timeupdate','durationchange','play','pause','ended','volumechange','loadedmetadata'])player.addEventListener(event,sync);
player.addEventListener('waiting',()=>{status.textContent='Loading film…';});player.addEventListener('playing',()=>{status.textContent='';});player.addEventListener('canplay',()=>{status.textContent='';});
// Native controls remain a no-JavaScript fallback. Enhanced controls sit below the picture.
player.controls=false;controls.hidden=false;sync();
for(const t of player.textTracks)t.mode='hidden';
player.addEventListener('loadedmetadata',()=>{for(const t of player.textTracks)t.mode='hidden';});
document.querySelectorAll('[data-time]').forEach(button=>button.addEventListener('click',()=>{
  const t=Number(button.dataset.time);player.pause();player.currentTime=t+.5;sync();
  document.getElementById('cue-status').textContent=`Cued to ${t} seconds. Press Play below the film to watch.`;
  frame.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth',block:'center'});play.focus({preventScroll:true});
}));
player.addEventListener('error',()=>{status.textContent='The film could not load. Use the download link below to watch it in your video player.';});
fetch('checks/loudness.json').then(r=>r.ok?r.json():Promise.reject()).then(d=>{document.getElementById('loudness').textContent=`${d.input_i} LUFS measured · stereo AAC`;}).catch(()=>{});
