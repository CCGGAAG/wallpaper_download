# -*- coding:utf-8 -*-
from wallpaper_download.CopyWallpaper import CopyWallpaper

# 配置并初始化
wallpaper_dir = "D:/Program Files (x86)/Steam/steamapps/workshop/content/431960"
output_dir = "D:/test"
test = CopyWallpaper(wallpaper_dir, output_dir)
# 全部类型拷贝
test.start_get_wallpaper_file(pkg_only=True, mp4_only=True, new_file_only=True)

# 仅图片类型拷贝
# test.start_get_wallpaper_file(pkg_only=True)

# 仅视频类型拷贝
# test.start_get_wallpaper_file(mp4_only=True)

# 统计不拷贝文件列表（把已经订阅的壁纸加入隔离名单，以后不会再下载）
# test.init_installed_file_list()
"""
new_file_only项是仅拷贝新订阅的壁纸文件，需要先把本地已经订阅的壁纸统计一下：init_installed_file_list
然后再运行获取壁纸文件命令时，就会跳过这些已经记录的壁纸文件

"""
