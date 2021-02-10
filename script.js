const markdownTable = require('markdown-table');
const fs = require('fs');
const data = fs.readFileSync('./douban250-in-bilibili.csv');
const rows = data.toString().split('\n');
rows.shift();
const table = rows.map(row => row.split(',').map(column => column.trim()));
const tableContentInMD = markdownTable([['排名', '电影名称', '豆瓣评分', '评分人数', '点评', '上映时间', '类型', '时长', '豆瓣', 'Bilibili'], ...table]);
const readme = tableContentInMD;
fs.writeFileSync('./README.md', readme, 'utf8');