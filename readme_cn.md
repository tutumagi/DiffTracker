## 需要：
1. python 3.x


## 用法
1. pip install -r ./requirements.txt
2. 修改 截图区域的坐标和大小
3. 修改 `src/env.example.yaml` 中的 `api_token` 为slack的应用token，并重命名为 env.yaml
4. 执行 `python src/diff.py` 进行调试

监控屏幕某块区域的变化，并将变化的内容发送到Slack

1. 定时截取屏幕上某块区域的内容
2. 将截图的图片和上一次的截图进行比对
3. 将差异的图像内容进行输出
4. 将图像内容发给Slack某个频道

## 注意
1. 截图区域确定后，被截图的区域不能被遮挡，不能移动

调试的话，可以先进行截图区域的修改，然后执行 `python src/diff.py`

## TODO
1. GUI进行截图区域的选择
2. 截图比对有时候不准。

