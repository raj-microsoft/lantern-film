// Headless Chromium-family renderer. A complete film is film.html, evaluated at seek(t).
const {chromium}=require('playwright-core');const {spawn}=require('child_process');const fs=require('fs');const path=require('path');const {once}=require('events');const {pathToFileURL}=require('url');
(async()=>{const four=process.argv.includes('--4k'),w=four?3840:1920,h=four?2160:1080,suffix=four?'-4k':'';
const browser=await chromium.launch({executablePath:process.env.CHROME_PATH||'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',headless:true,args:['--allow-file-access-from-files']});
const page=await browser.newPage({viewport:{width:w,height:h},deviceScaleFactor:1});await page.goto(pathToFileURL(path.resolve('film.html')).href+'?render=1');await page.evaluate(()=>window.filmReady);await page.evaluate(([w,h])=>window.configureFilm(w,h),[w,h]);
// Verify deterministic seek, and prove that temporal samples change moving geometry.
const hashes=await page.evaluate(()=>{seek(4.2,4);const a=document.querySelector('canvas').toDataURL();seek(12);seek(4.2,4);const b=document.querySelector('canvas').toDataURL();seek(4.2,1);const c=document.querySelector('canvas').toDataURL();return {deterministic:a===b,motionBlurChangesPixels:a!==c};});
if(!hashes.deterministic||!hashes.motionBlurChangesPixels)throw Error('Determinism/blur check failed');
const encoder=spawn('ffmpeg',['-y','-loglevel','error','-f','image2pipe','-vcodec','png','-r','30','-i','-','-an','-c:v','libx264','-preset','fast','-crf',four?'22':'20','-pix_fmt','yuv420p',`assets/silent${suffix}.mp4`],{stdio:['pipe','inherit','inherit']});const done=once(encoder,'close');
for(let i=0;i<900;i++){
 const data=await page.evaluate(t=>{seek(t,4);return document.querySelector('canvas').toDataURL('image/png').split(',')[1];},i/30);
 if(!encoder.stdin.write(Buffer.from(data,'base64')))await once(encoder.stdin,'drain');
 if(!four&&[60,180,330,510,675,840].includes(i)){
 const jpg=await page.evaluate(()=>{const out=document.createElement('canvas');out.width=960;out.height=540;out.getContext('2d').drawImage(document.querySelector('canvas'),0,0,960,540);return out.toDataURL('image/jpeg',.94).split(',')[1];});fs.writeFileSync(`assets/shot-${Math.floor(i/150)+1}.jpg`,Buffer.from(jpg,'base64'));
 if(i===60){const poster=await page.evaluate(()=>document.querySelector('canvas').toDataURL('image/jpeg',.96).split(',')[1]);fs.writeFileSync('assets/poster.jpg',Buffer.from(poster,'base64'));}}
 if(i%150===0)console.log(`${w}x${h}: ${i}/900 frames`);
}
encoder.stdin.end();const [code]=await done;if(code)throw Error('ffmpeg exited '+code);await browser.close();fs.writeFileSync(`checks/render${suffix}.json`,JSON.stringify({engine:'Headless Edge (Chromium)',entry:'film.html',width:w,height:h,frames:900,fps:30,subframeSamples:4,shutterSeconds:1/60,captions:'Drawn after temporal accumulation',...hashes},null,2));
})().catch(e=>{console.error(e);process.exit(1);});
