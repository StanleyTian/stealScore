//study: https://molunerfinn.com/nodejs-1/
const cheerio   = require('cheerio');
const request   = require('sync-request');
const iconv     = require('iconv-lite');
const fs        = require('fs');
const fse = require('fs-extra');
const download  = require('download');
const events    = require("events");
const superagent = require('superagent');
const charset = require('superagent-charset');
charset(superagent);
//var emitter = new events.EventEmitter();

//setCookie ();
//emitter.on("setCookie", getPost);    //监听setCookie事件
// var url = 'http://bbs.guitarera.com/thread-2049-1-1.html'; //李斯特 page 1
// var html = '';
// var cookie;

//readPost(str);
for (var ai=1;ai<=7;ai++) {
    var url = 'http://bbs.guitarera.com/thread-2049-'+ai+'-1.html';
    crawlPage(url);
}
function readPost(url,html) {
    var fileName="";
    var fileContent = "";
    fileContent += "[原文链接]("+url+")\r\r";
    var $ = cheerio.load(html);
    fileName += $("#thread_subject").text();
    fileName += "page-"+$("#pgt .pgt .pg>strong").text();
    $("#postlist").children().each(function(i, elem) {
        var pattern = /\bpost_\d{3,10}\b/;
        var post_id = $(this).attr('id') ;
        if(pattern.test(post_id) == true){
            //匹配帖子id
            //console.log($(this).attr('id'));

            var postTitle = $("#"+ post_id+" .pcb h2").text();
            var postContent = $("#"+ post_id+" .pcb .t_fsz").text();
            //var postContent = $("#postmessage_"+post_id).text();
            console.log(postTitle);
            fileContent+=postTitle+"\r\r";
            var allLinks = $("#"+ post_id+" .attnm a").map(function () {
                return {
                    "url":"http://bbs.guitarera.com/"+$(this).attr("href"),
                    "text":$(this).text()
                };
            });
            fileContent+="曲谱链接\r\r";
            for(var i=0;i<allLinks.length;i++){
                fileContent += "["+allLinks[i].text+"]("+allLinks[i].url+")\r\r";
            }

            //fileContent+=postContent+"\r\r";
            fileContent+="-------------------"+"\r";
            //
            //   download(downloadLink, 'dist').then(() => {
            //     console.log('done!');
            // });
        }
    });
    fse.ensureDirSync("./score");
    fs.writeFileSync("./score/"+fileName+".md",fileContent);
}

function setCookie () {
    superagent.post('http://bbs.guitarera.com/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes')  //登录提交地址
        .type("form")
        .send({username:"1016zym"})
        .send({password:"hebe1016"})
        .send({quickforward:"yes"})
        .send({handlekey:"ls"})
        .end(function(err, res){
            if (err) throw err;
            cookie = res.header['set-cookie']             //从response中得到cookie
            console.log(cookie);
            emitter.emit("setCookie", cookie)
        })
}

function getPost () {
    var cookieStr = "";
    for(var i=0;i<cookie.length;i++)
    {
        cookieStr += cookie[i]+";";
    }
    console.log(cookieStr);
    superagent.get("http://bbs.guitarera.com/thread-2049-1-1.html")             //随便论坛里的一个地址
        .charset('gbk')
        .set("Cookie", cookieStr)                 //在resquest中设置得到的cookie，只设置第四个足以（具体情况具体分析）
        .set("Referer","http://bbs.guitarera.com/forum.php")
        .set("Host","bbs.guitarera.com")
        .end(function(err, res){
            if (err){
                throw err;
            };
            //do something
            //console.log(res);

            readPost(res.text);
        })
};

function crawlPage(url) {
    superagent.get(url)             //随便论坛里的一个地址
        .charset('gbk')
        .end(function(err, res){
            if (err){
                throw err;
            }
            readPost(url,res.text);
        })
}