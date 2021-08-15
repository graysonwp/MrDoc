#!bin/bash
# 常量数据
# 当前时间
CURRENT_TIME=`date "+%Y-%m-%d %H:%M:%S"`
# 项目根目录
BASE_PATH=/usr/local/projects/MrDoc

echo "0. 开始更新"

echo "1. 合并 upstream 更新"
git merge upstream/master

echo "2. 添加所有新增文件"
git add -A ${BASE_PATH}/

echo "3. 提交更新"
git commit -a -m "Auto updated, current time is ${CURRENT_TIME}"

echo "4. 推送到远端"
git push origin master

echo "5. 更新完成"
