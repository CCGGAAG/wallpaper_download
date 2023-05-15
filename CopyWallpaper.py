# -*- coding:utf-8 -*-
import os
import shutil
import yaml
import hashlib
import random


class CopyWallpaper:

    def __init__(self, steam_url, copy_dir):
        """
        类的初始化，两个地址必需传递为本地电脑的绝对路径
        :param steam_url: wallpaper的数据文件夹，例如：D:/**/Steam/steamapps/workshop/content/431960
        :param copy_dir:  你要转移存储文件的地址
        """
        self.steam_url = steam_url
        self.copy_dir = copy_dir
        self.file_format = [".mp4", ".MP4", ".MOV", ".mov", ".avi", ".AVI",  ".webm", ".WEBM", ".pkg"]
        self.video_format = [".mp4", ".MP4", ".MOV", ".mov", ".avi", ".AVI", ".webm", ".WEBM", ".mp3"]
        self.pkg_file_format = [".png", ".PNG", ".jpg", ".JPG", ".jpeg", ".JPEG", "gif", "GIF"]
        if "img" not in os.listdir(self.copy_dir):
            os.makedirs(self.copy_dir + "/img")

    def get_repkg_img(self, list_pkg):
        """
        通过本地的pkg文件地址列表，将pkg解压后的图片文件移动到指定文件夹（copy_dir）下
        :param list_pkg: 本地的pkg文件地址列表
        :return:
        """
        pkg_path = os.getcwd() + "/repkg"
        base_driver = pkg_path[0]
        for i in list_pkg:
            if "dispose" not in os.listdir(pkg_path):
                os.makedirs(pkg_path + "/dispose")
            self.file_copy([i], "./repkg/dispose")
            print("-----------------------------------------------------------")
            print("pkg文件%s" % i)
            pkg_name = i[str(i).rfind("/") + 1:]
            cmd_line = "%s: && cd %s && RePKG.exe extract -o ./dispose ./dispose/%s" % (base_driver, pkg_path, pkg_name)
            os.system(cmd_line)
            img_list = self.get_format_file_list(dir_path=pkg_path + "/dispose/materials", file_format=self.pkg_file_format)
            [self.file_copy([j], self.copy_dir + "/img") for j in img_list if os.path.getsize(j) >= 100000]
            shutil.rmtree("./repkg/dispose/")

    def file_copy(self, file_list, copy_dir=None):
        """
        一个复制文件的方法，把列表中地址的文件拷贝到指定文件夹
        :param file_list: 一个本地文件地址的列表
        :param copy_dir: 默认是self.copy_dir
        :return:
        """
        if copy_dir is None:
            copy_dir = self.copy_dir
        for i in file_list:
            copy_file_list = os.listdir(copy_dir)
            file_name = i[str(i).rfind("/") + 1:]
            if file_name in copy_file_list:
                new_name = str(i).replace(file_name, ("重复%s" % random.randint(10000, 19999) + file_name))
                shutil.copy(i, new_name)
                shutil.move(new_name, copy_dir)
                print("移动文件：%s" % new_name)
            else:
                shutil.copy(i, copy_dir)
                print("拷贝文件：%s" % i)

    def get_format_file_list(self, dir_path, file_list=None, file_format=None):
        """
        通过一个目录地址，递归获取目录下所有‘规定格式’的文件的地址（默认文件类型：视频、图片、pkg）
        :param dir_path:文件夹绝对地址
        :param file_list:默认None
        :param file_format:默认None
        :return: file_list
        """
        if file_list is None:
            file_list = []
        if file_format is None:
            file_format = self.file_format + self.pkg_file_format

        file_in_dir_list = os.listdir(dir_path)
        for file_name in file_in_dir_list:
            url_join = dir_path + '/' + file_name
            file_type = os.path.splitext(url_join)[1]
            if os.path.isdir(url_join):
                self.get_format_file_list(url_join, file_list)
            elif file_type in file_format:
                file_list.append(url_join)
            else:
                pass
        return file_list

    def split_list(self, file_list):
        """
        处理单个wallpaper地址列表，变为视频和pkg文件地址的两个列表
        :param file_list:
        :return: mp4_list, pkg_list
        """
        list_mp4 = [x for x in file_list if os.path.splitext(x)[1] in self.video_format]
        list_pkg = [y for y in file_list if ".pkg" == os.path.splitext(y)[1]]
        img = [z for z in file_list if os.path.splitext(z)[1] in self.pkg_file_format]
        list_img = [m for m in img if m.find("preview.jpg") == -1]
        return list_mp4, list_pkg, list_img

    def start_get_wallpaper_file(self, pkg_only=False, mp4_only=False, new_file_only=False):
        """
        一键获取所有wallpaper文件
        :param pkg_only: 是否获取pkg图片文件
        :param mp4_only: 是否获取视频文件
        :param new_file_only: 是否仅获取新订阅的文件
        :return:
        """
        whole_file_list = self.get_format_file_list(self.steam_url)
        if new_file_only:
            self.init_installed_file_list()
            with open("./repkg/file_path_list.yaml", 'rb') as f:
                path_list = yaml.load(f, Loader=yaml.FullLoader)
            with open("./repkg/md5_list.yaml", 'rb') as f:
                md5_list = yaml.load(f, Loader=yaml.FullLoader)
            update_file_list = [i for i in whole_file_list if i not in path_list and self.get_md5(i) not in md5_list]
            print(update_file_list)
        else:
            update_file_list = whole_file_list
        list_mp4, list_pkg, list_img = self.split_list(update_file_list)
        if pkg_only:
            self.get_repkg_img(list_pkg)
            [self.file_copy([j], self.copy_dir + "/img") for j in list_img if os.path.getsize(j) >= 100000]
        if mp4_only:
            self.file_copy(list_mp4)
        if not pkg_only and not mp4_only:
            print("请设置拷贝图片还是视频")

    @staticmethod
    def get_md5(filename):
        """
        获取文件md5值
        :param filename: 文件路径
        :return: md5值
        """
        md5_handle = hashlib.md5()
        md5_file = open(filename, "rb")
        md5_handle.update(md5_file.read())
        md5_file.close()
        md5_value = md5_handle.hexdigest()
        return md5_value

    def init_installed_file_list(self):
        """初始化已经订阅的所有壁纸信息，并保存为文件"""
        whole_file_list = self.get_format_file_list(self.steam_url)
        if "file_path_list.yaml" not in os.listdir("./repkg"):
            print("新建file_path文件")
            fd = open("./repkg/file_path_list.yaml", mode="w", encoding="utf-8")
            fd.close()
            data = whole_file_list
            fw = open("./repkg/file_path_list.yaml", 'a', encoding='utf-8')
            yaml.dump(data, fw)
            fw.close()
        if "md5_list.yaml" not in os.listdir("./repkg"):
            print("新建md5文件")
            fd = open("./repkg/md5_list.yaml", mode="w", encoding="utf-8")
            fd.close()
            data = [self.get_md5(i) for i in whole_file_list]
            fw = open("./repkg/md5_list.yaml", 'a', encoding='utf-8')
            yaml.dump(data, fw)
            fw.close()

            
if __name__ == '__main__':
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
