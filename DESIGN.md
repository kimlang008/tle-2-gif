# TLE2GIF by matplotlib 计划书
## 用途
接受用户给出含卫星tle数据的网址，并绘制gif图直观展现卫星轨迹
命令行
用
```powershell
python main.py draw https://网站
```
启动程序

| 参数    | 类型   | 位置/选项 | 必给？ | 默认值 | 说明                 |
| ------- | ------ | --------- | ------ | ------ | -------------------- |
| draw    | 子命令 | 子命令    | 是     | ——     | 给定tle数据画gif图   |
| tle地址 | 网址   | 位置      | 是     | ——     | 轨道数据所在地址     |
| --debug | 开关   | 选项      | 否     | 关闭   | 给出计算所得坐标参数 |

## 输入
1. 输入源

| 卫星名称 | 网址                                                               |
| -------- | ------------------------------------------------------------------ |
| ISS      | https://celestrak.org/NORAD/elements/gp.php?CATNR=25544&FORMAT=TLE |
| CSS(问天)      | https://celestrak.org/NORAD/elements/gp.php?CATNR=53239&FORMAT=TLE |

2. 程序获取数据方式： 
## 程序结构
- 搜录->计算->画图
- 先用下载函数，下载tle信息
  - 30s取一个点，每个点包含经纬度，时间，高度
  - 装入tuple
  - 单位为度
  - 东经为正
- 计算与画图分为独立的两部分
- 计算函数 输入tuple输出坐标参数
- 画图函数 输入坐标参数，输出图像,画世界地图为底图


## 输出
- 输出内容
  - 卫星名称及tle信息
  - 坐标信息
  - gif图像
- 输出方式
  - 显式：图像，名称
  - 隐式：参数
  - 使用者看到-gif图像
  - 使用者可以调取坐标参数
- 退出码约定
  - 通过=0
  - 由程序自身检查出的错误=3
  - argparse检验异常=2
  
## 画图层
- 函数名 plot_ground_track
- 返回gif,返回路径给os.path.exist
- 只向其中输入画图参数与卫星名
- 检验项目
   1. 文件存在
      - os.path.exists 
   2. 合法GIF，帧数正确，尺寸正确
      -  PIL检测
- tmp_path将测试产生文件放入独立目录
  
## 计算函数
- 默认iss
- 函数名para_calc
- download将三行传递给extract，extract再传递给calc
- 为什么不能读TlePara?
- 时间用datetime表示
- 步长t按design
- 返回lon lat height
- time zone UTC
- 时间返回原始数组
- 验收
  1. 高度自洽
  2. 纬度在倾角内
  3. 官方示例对照


## 工具
### 从网页调取数据
标准库urllib.request
### 计算工具 
python+skyfield

### 绘图工具
matplotlib

## 验收标准
- 要求，不随便吐traceback，反馈要清晰明确
1. 检验用户给的网站是否有包含tle信息
  - 信息有误，返回"所给内容不符合程序要求，请给出含轨道参数的信息"退出码3
2. 网络渠道是否畅通
  - 网络阻塞，返回"网络异常"以退出码3退出
3. 是否用对库
  - 距离epoch24h内相对skyfield官方示例数值误差<=10km
4. 计算是否精确
   - 与Heavens-Above的误差(用大圆距离)<0.5度
5. 画图过程准确度
  - 步长30秒，10fps，180帧，18秒播完

## 思考
