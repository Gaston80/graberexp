
N = 0
CamCount = 1
start = 1
camlist = []
var header = document.getElementById("header");
var radio = document.getElementById("radio");
var cmdLine = document.getElementById("cmd");
var cmdResp = document.getElementById("resp");
var CamTable = document.getElementById("CamTable");
var CamInfo = document.getElementById("info");
var ImpTable = document.getElementById("ImpTable");

evtSource = new EventSource("/text_stream?N=0");
evtSource.onmessage = setTable;

function setTable(event)
{
    let text = event.data;
    var data = JSON.parse(text);
    CamCount = data.CamsCount;
    delete data['Type']
    delete data['CamsCount']
    var important = data['important']
    delete data['important']
    ImpTable.innerHTML = table(important)
    CamInfo.textContent = data.Info
    delete data['Info']
    camlist = data['camlist']
    if (start)
    {
        setStart(camlist)
    }
    delete data['camlist']
    CamTable.innerHTML = table(data)
};

function setStart(camlist)
{
    start = 0;
    cloneVideo(camlist);
    camlist.push('Всем');
    camlist.forEach(addCam);
}

function cloneVideo(camlist)
{
    var baseBlock = document.getElementById("VideoBlock");
    var camVideoT = baseBlock.cloneNode(true);
    baseBlock.remove()
    var outputContainer = document.getElementById("VideoBlocks");
    for(var i = 0; i < camlist.length; i++)
    {
        var camVideo = camVideoT.cloneNode(true);
        camVideo.querySelector("h4").textContent = camlist[i];
        camVideo.querySelector("img").src = "/video_feed?W=600&N="+i
        camVideo.querySelector("a").href = "/video_feed?N="+i
        camVideo.querySelector(".download").href = "/img?N="+i
        camVideo.querySelector(".download").download = camlist[i]+'.jpg'
        camVideo.querySelector(".nodelist").href = "/nodelist?N="+i
        outputContainer.appendChild(camVideo);
    }

}

function addCam(name)
{
    var radioButton = document.createElement("input");
    radioButton.type = "radio";
    radioButton.name = "CameraSelect";
    radioButton.value = name;
    var label = document.createElement("label");
    label.textContent = name;
    radio.appendChild(radioButton);
    radio.appendChild(label);
}


function cmdSend(cmd = '')
{
    var cam = document.querySelector('input[name="CameraSelect"]:checked');
    all = false;
    NN = 0;
    if (cam)
    {
        name = cam.value;
        NN = camlist.indexOf(name);
        if (name == 'Всем')
        {
            NN = 0;
            all = true;
        }
    }
    else
    {
        all = true;
        NN = 0;
    }
    if (cmd == '') cmd = cmdLine.value;
    if (cmd == '') cmd = 'x'
    url = "/cmd?N="+NN+"&cmd="+cmd+'&all='+all
    fetch(url)
        .then(response => response.json())
        .then(data =>{cmdResp.innerHTML = cmd+' => '+data.resp+'<br>'+cmdResp.innerHTML})
        .catch(error => {console.error('Произошла ошибка:', error);});
}

function table(data)
{
    let res = '';
    for (let key in data)
    {
        var span = 0
        let val = data[key];
        if ((typeof val === 'string') && (val.substring(0, 3) == '---'))
        {
            res += '<tr><td colspan = "100" align="center"><h5>'+key+'</h5></td></tr>'
            continue
        }
        res += '<tr><td>' + key + '</td>';
        if (!Array.isArray(val))
        {
            val = [val]
            span = 1000
        }
        for(var i = 0; i < val.length; i++)
        {
            res += '<td colspan = "'+span+'">' + bool2htm(val[i]) + '</td>'
        }
        res += '</tr>';
    }
    return res
}
function bool2htm(val)
{
    let out = val
    if (typeof val == "boolean")
    {
        out = '<font color = "red">X</font>'
        if (val) out = '<font color = "green">V</font>'
    }
    return out
 }
function getPhotos()
{
    var photos = document.getElementById("photos");
    fetch("/photos")
    .then(response => response.text())
    .then(data => {photos.innerHTML = data;})
    .catch(error => {console.error("Ошибка", error)});
}
