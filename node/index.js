const tmi = require('tmi.js');

const handleMessage = async (message)=>{
    let stopDefault = await fetch("http://0.0.0.0/sys", {
                method: "POST",
                body: new URLSearchParams({"status": "stop"})
            });
            console.log(await stopDefault)
    let sendMessage = await fetch("http://0.0.0.0/redemption",{
        method: "POST",
        body: new URLSearchParams({"redemption": message})
    })
    console.log(await sendMessage)
    let startDefault = await fetch("http://0.0.0.0/sys", {
        method: "POST",
        body: new URLSearchParams({"status": "start"})
    }); 
    console.log(startDefault)
}


const client = new tmi.Client({
	channels: [ 'sfmoe' ]
});

client.connect();
console.log(client)
client.on('message', (channel, tags, message, self) => {
    if(tags['custom-reward-id'] === "86b6fceb-becb-44fe-aa24-bed339f5d41e"){
    let emotes = new Map();
    if(tags['emotes'] !=null){
            let start = 0;
            let end = 0;
            for (let [key, value] of Object.entries(tags['emotes'])) {
                let url = `https://static-cdn.jtvnw.net/emoticons/v2/${key}/default/dark/2.0`;
                console.log(url)
                let splitIndex = value[0].split("-") 
                
                    start = parseInt(splitIndex[0])+1
                    end = parseInt(splitIndex[1])+2
                let newkey =  message.substring(start, end)
                
                emotes.set(newkey, url)

            
            }

            emotes.forEach((val, key, map)=>{
                message = message.replace(key, val)
            })
            
            
        }
        
        handleMessage(message)

    }
});