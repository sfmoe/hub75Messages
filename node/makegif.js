const Canvas = require("@napi-rs/canvas");
const path  = require("path");
const sharp = require("sharp");
const GIF = require("sharp-gif");

Canvas.GlobalFonts.registerFromPath(path.join(__dirname, 'fonts', 'NotoColorEmoji-Regular.ttf'), 'Noto Color Emoji')

const width = 64,  height = 32;
let font = 20, x = 64, y = 32;

let canvas = Canvas.createCanvas(width, height);
let ctx = canvas.getContext('2d');
ctx.font = `${font}px 'FreeSans', 'Noto Color Emoji'`;
ctx.textBaseline = 'top';
//ff8c00 dark orange


const animate = (str)=>{
  // creates array of canvas elements as buffers
  const frames = [];
  let ix = x;

  while(ix > (0 - ctx.measureText(str).width) ){
    ctx.clearRect(0, 0, width, height);   
    ctx.fillStyle = "#000000";
    ctx.fillRect(0, 0, width, height);
    ctx.fillStyle = "#FFFFFF";
    ctx.fillText(str, ix, (height-font)/2);
    frames.push(sharp(canvas.toBuffer("image/png")))
    // 5 pixel per frame
    ix += -5
  }
  return frames;
}

let f = animate(" this is a test with emoji 🔥 ✔️");


(async ()=>{ 
  let image = await GIF.createGif({delay: 200}).addFrame(f).toSharp();
image.toFile("../images/frame.gif")
})()







