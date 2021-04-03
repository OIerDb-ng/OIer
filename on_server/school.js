var contest_names = ["NOIP普及", "NOIP提高", "CSP入门", "CSP提高", "NOIP", "APIO", "CTSC", "NOI", "NOID类", "WC"];
var award_desc = { "NOIP普及": ["一等奖", "二等奖", "三等奖"], "CSP入门": ["一等", "二等", "三等"], "CSP提高": ["一等", "二等", "三等"], "NOIP提高": ["一等奖", "二等奖", "三等奖"], "NOIP": ["一等奖", "二等奖", "三等奖"], "APIO": ["金牌", "银牌", "铜牌"], "CTSC": ["金牌", "银牌", "铜牌"], "NOI": ["金牌", "银牌", "铜牌"], "NOID类": ["金牌", "银牌", "铜牌"], "WC": ["金牌", "银牌", "铜牌"] };
var data_year_range = {
    "NOIP普及": [2013, 2018], "NOIP提高": [2010, 2018],
    "CSP入门": [2019, 2020], "CSP提高": [2019, 2020],
    "NOIP": [2020, 2020], "APIO": [2010, 2020],
    "CTSC": [2010, 2019], "NOI": [2009, 2020],
    "NOID类": [2010, 2020], "WC": [2015, 2021]
};
var grades = ["一年级", "二年级", "三年级", "四年级", "五年级", "六年级", "初一", "初二", "初三", "高一", "高二", "高三"];
var cacheSchoolData;

function deepClone(obj) {
    let _obj = JSON.stringify(obj),
        objClone = JSON.parse(_obj);
    return objClone
}

function showSchoolAwards(s) {
    config["data"]["datasets"] = [];
    var cur_year = [];
    let [begin, end] = data_year_range[s];
    for (var i = begin; i <= end; i++)cur_year.push(i.toString());
    for (var i = 0; i < document.getElementById("con-group").childElementCount; i++) {
        if (document.getElementById("con-group").children[i].className.includes("minebtn-ac"))
            document.getElementById("con-group").children[i].className = "btn minebtn";
    }
    if (document.getElementById(s).className.includes("minebtn-ac")) {

    } else {
        config["data"]["labels"] = deepClone(cur_year);
        document.getElementById(s).className = "btn minebtn-ac";
        config["data"]["datasets"] = deepClone(model);
        for (var i = 0; i <= 2; i++) {
            config["data"]["datasets"][i]["data"] = []
            config["data"]["datasets"][i]["label"] = s + award_desc[s][i];
            for (var j in cur_year) {
                cy = cur_year[j];
                if (cy in cacheSchoolData["awards"][s])
                    config["data"]["datasets"][i]["data"].push(cacheSchoolData["awards"][s][cy][i]);
                else
                    config["data"]["datasets"][i]["data"].push(0);
            }
        }

    }
    //var ctx = document.getElementById('canvas').getContext('2d');
    window.myLine.update();
}

async function showSchoolInfo(s, p) {
    $('#sch_desc').html('<img src = "assets/loading.svg" width = 45px/>');
    $('#con-group').html('');
    $('#school_view').attr('style', 'flex-flow: column;display:flex');
    $('#sch_name').html(p);
    config["data"]["datasets"] = [];
    window.myLine.update();
    let _path = location.pathname;
    _path = _path.substr(0, _path.lastIndexOf('/'));
    if (!_path.endsWith('/')) _path += '/';
    let target = new URL(location.protocol + '//' + location.host + _path + 'school.php');
    target.searchParams.append('id', s.toString());

    try {
        let result = await fetch(target);
        let data = await result.json();
        let school = data['result'][0]
        school["name"] = eval(school["name"]);
        school["awards"] = eval("(" + school["awards"] + ")");
        c_desc = "";
        if (school["name"].length > 2) {
            c_desc = "<p>又名";
            for (var i in school["name"]) {
                var cn = school["name"][i];
                if (cn != p) c_desc += cn + ","
            }
            c_desc = c_desc.substr(0, c_desc.length - 1) + "。</p>";
        }
        c_desc += `<p>综合评分: <b>${school["rating"]}</b>，综合评级<b>${school["division"]}</b>。`;
        $('#sch_desc').html(c_desc);
        let buttons = '';
        for (var i in contest_names) {
            var cur_con = contest_names[i];
            if (cur_con in school["awards"]) {
                buttons +=
                    `<button type="button" class="btn minebtn" id="${cur_con}"
                        onclick = "showSchoolAwards('${cur_con}')">
                        ${cur_con}
                    </button>`;
            } else {
                buttons +=
                    `<button type="button" class="btn minebtn disabled">
                        ${cur_con}
                    </button>`;
            }
            $('#con-group').html(buttons);
        }
        cacheSchoolData = school;
    } catch (err) { console.error(err); }
}
