var superagent = require('superagent');
var events = require("events");
const charset = require('superagent-charset');
charset(superagent);

var emitter = new events.EventEmitter()

setCookeie ();
emitter.on("setCookeie", getTitles)            //监听setCookeie事件



function setCookeie () {
    superagent.post('http://bbs.guitarera.com/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes')  //登录提交地址
        .type("form")
        .charset('gbk')
        .send({username:"1016zym"})
        .send({password:"2424d24be57cacd465d3a574b4dbfafd"})
        .send({quickforward:"yes"})
        .send({handlekey:"ls"})
        .end(function(err, res){
            if (err) throw err;
            var cookie = res.header['set-cookie']             //从response中得到cookie
            console.log(res);
            console.log(res.text);
            //console.log(cookie);
            //emitter.emit("setCookeie", cookie)
        })
}

function getTitles (cookie) {
    superagent.get("http://bbs.guitarera.com/forum.php")             //随便论坛里的一个地址
        .set("Cookie", cookie[3])                 //在resquest中设置得到的cookie，只设置第四个足以（具体情况具体分析）
        .end(function(err, res){
            if (err){
                throw err;
            };
            //do something
        })
};

var c = [ 'qOGl_2132_saltkey=y8s661AU; expires=Sun, 02-Apr-2017 06:10:53 GMT; path=/; httponly',
    'qOGl_2132_lastvisit=1488517853; expires=Sun, 02-Apr-2017 06:10:53 GMT; path=/',
    'qOGl_2132_sid=bG4NX4; expires=Sat, 04-Mar-2017 06:10:53 GMT; path=/',
    'qOGl_2132_lastact=1488521453%09forum.php%09; expires=Sat, 04-Mar-2017 06:10:53 GMT; path=/',
    'safedog-flow-item=921DF2A466B4BFF7FD6B8D7328BE4597; expires=Fri, 3-Mar-2017 15:59:53 GMT; domain=guitarera.com; path=/' ];