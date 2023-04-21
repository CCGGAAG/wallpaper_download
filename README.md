# wallpaper_download
download pic and vedio files from wallpaper
### 项目介绍
来自repkg包的一个二次开发  
repkg包地址：https://github.com/notscuffed/repkg/releases 

- 本项目是一个二次开发项目
- 需要电脑本地有python环境
- 可以下载wallpaper的所有视频、图片资源
- 需要配置两个参数：你的wallpaper软件本地文件夹地址、资源要拷贝至的文件夹

### 使用说明
1.首先进入当前项目的命令行页面，执行pip install -r requirements.txt
或者 pip install PyYAML,因为本项目只使用了这一个第三方库。  

2.打开srart.py文件，将两个参数改成你本地的，
- wallpaper_dir：你的本地wallpaper软件文件夹地址
- output_dir：你想拷贝到的文件夹地址  

3.使用python运行start.py文件即可  

4.如果你想要省劲，修改paper.bat文件中的cmd命令，也就是进入当前项目文件夹，并且运行start.py文件，把这个bat命令做成一个快捷方式，这样只用点击bat命令就可以拷贝文件资源了，非常方便！！！

5.当你多次运行这个文件后，会发现每次都将所有资源下载了，所以在start.py文件中，将test.init_installed_file_list()的注释去掉，然后运行一下即可，会生成一个当前订阅的资源名单，以后再拷贝文件的话，会跳过名单上的资源。
### 项目参数
执行获取文件的方法start_get_wallpaper_file()：  
- pkg_only，默认为True，指定是否解压并拷贝pkg封装的图片文件
- mp4_only，默认为True，指定是否拷贝视频文件
- new_file_only，默认为True，名单中的资源不再下载，只下载名单上没有的


将已经订阅的壁纸放入下载名单中init_installed_file_list()

