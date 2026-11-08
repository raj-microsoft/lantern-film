const player=document.getElementById('player');
// Captions are burned into every frame; the accessible track is available but not doubled.
player.addEventListener('loadedmetadata',()=>{for(const t of player.textTracks)t.mode='hidden';});
document.querySelectorAll('[data-time]').forEach(button=>button.addEventListener('click',()=>{
  const time=Number(button.dataset.time);player.pause();player.currentTime=time+.5;
  document.getElementById('cue-status').textContent=`Cued to ${time} seconds. Press play in the film to watch.`;
  player.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth',block:'center'});player.focus();
}));
player.addEventListener('error',()=>{document.getElementById('cue-status').textContent='The film could not load. Use the download link to watch it in your video player.';});
fetch('checks/loudness.json').then(r=>r.ok?r.json():Promise.reject()).then(d=>{document.getElementById('loudness').textContent=`${d.input_i} LUFS measured · stereo AAC`;}).catch(()=>{});
