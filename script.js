const markdownTable = require('markdown-table');
const fs = require('fs');
const data = fs.readFileSync('./douban250-in-bilibili.csv');
const rows = data.toString().split('\n');
const len = rows.shift().length;
const table = rows.map(row => row.split(',').map(column => column.trim()));
const newTable = table.map(row => {
  const rate = row[2];
  const doubanLink = row[5];
  const bilibiliLink = row[6];
  return [
    row[0],
    row[1],
    row[3],
    `[![](https://shields.io/badge/豆瓣-${rate}-00B51D?logo=douban&logoColor=white)](${doubanLink})`,
    `[![](https://shields.io/badge/-哔哩哔哩-fb7299?logo=bilibili&logoColor=white)](${bilibiliLink})`,
  ];
});
const tableContentInMD = markdownTable([['排名', '电影名称', '推荐语', '豆瓣', '哔哩哔哩'], ...newTable]);

const readme = `
# B 站豆瓣电影 Top250

本仓库整理了 B 站能够观看的「**豆瓣电影 Top250 榜单**」影片，点击 Badge 可跳转至相应的电影首页，👏 欢迎一同维护。

## 电影列表

${tableContentInMD}

## 如何维护

1. 在[./douban250-in-bilibili.csv](./douban250-in-bilibili.csv) 中填入相应的电影简介以及名称。
2. 提交 PR
3. (自动) PR 被 merge 之后 README 通过 [./script.js](./script.js) 生成

## Thanks

感谢 [@mrchi](https://www.v2ex.com/t/752717) 整理的 [Google Docs](https://docs.google.com/spreadsheets/d/150UlNx0rv-wdattxUTuvRKTjAUMYWCWmBnHQZ8FV5Kg/edit#gid=0)。

`;


fs.writeFileSync('./README.md', readme, 'utf8');
