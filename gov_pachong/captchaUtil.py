from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

import time
import re
import requests
from io import BytesIO
from PIL import Image
import random
# 这里以虎嗅网为例，虎嗅网用的滑动验证码是由极验提供的。下面叙述下破解滑块验证码的难点：
# 1、得到完整的验证码图片：难点存在于网页中直接得到的图片是乱的，需要我们自己重新进行裁剪和拼接。
# 2、获取缺口的距离：之所以说这个是难点，是考虑到有些人对图片处理不熟悉，如果有点图片处理的基础，这个并不难。
# 3、模拟人为的滑块移动轨迹：难点在于不合理的移动轨迹会被极验判断为非人类操作。

#没有用截图的方式，因为截图并不能获取仅有缺口的图片，图片中还有拖动的缺失块，而图片是一系列的list小图片拼接的，只能做图片还原

class SlipCaptcha(object):
    user ="13590170246"
    pwd ="zuobiao888"
    def __init__(self):
        """
        初始化界面,初始化了driver对象和wait对象,以及传入了一个url地址
        """
        self.url = 'https://www.tianyancha.com/'
        option = Options()
        # option.add_argument('--window-size=1332,700')
        # 去掉浏览器默认的 “chrome正受到自动测试软件的控制”信息栏显示问
        # option.add_argument('--disable-infobars')这个选项已废弃
        option.add_experimental_option("excludeSwitches", ['enable-automation']);
        # option.add_argument('headless')
        option.add_argument('incognito')
        self.driver = webdriver.Chrome(r"C:\软件\chromedriver_win32\chromedriver.exe",chrome_options=option)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 50)

    def home_page(self):
        """
        主要流程实施的函数
        1:driver.get函数先到达虎嗅首页面
        2:点击头像按钮，就会弹出登录页面，这时手动输入手机号码，点击发送验证码，弹出验证图框
        3:获取验证码的图片,图片有两份,一份是有缺口的,一份没有缺口
        4:获得的两份图片是被打乱,需要我们根据坐标信息,重新裁剪拼接
        5:拼接后,比较两份图片的区别,得到缺口的x方向的距离
        6:依据得到的距离,滑动滑块,由于存在对滑块轨迹的限制.所以我们还要设置如何活动,即以什么样的速度,加速度来滑动.
        :return:
        """
        self.driver.get(self.url)

        # login_button = self.driver.find_element_by_xpath('//img[@src="https://s1-www.huxiucdn.com/public/user.png"]')
        login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='link-white']")))
        # login_button = self.driver.find_element_by_xpath('//a[@class="link-white"]')
        login_button.click()
        button2 = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//div[@class="title-tab text-center"]/descendant::div[2]')))
        button2.click()
        # 账号密码登录框
        time.sleep(2)
        input_user = self.driver.find_element_by_xpath('//input[@id="mobile"]').clear()
        input_psw = self.driver.find_element_by_xpath('//input[@id="password"]').clear()
        self.driver.find_element_by_xpath('//input[@id="mobile"]').send_keys(self.user)  # 发送登录账号
        self.driver.find_element_by_xpath('//input[@id="password"]').send_keys(self.pwd)
        time.sleep(2)  # 等待 一秒 方式被识别为机器人
        login = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//div[@class="sign-in"]/div[2]/div[2]')))
        # login = self.driver.find_element_by_xpath('//div[@class="sign-in"]/div[2]/div[2]').click()
        login.click()

        gap_image_position, nogap_image_position, gap_image_url, nogap_image_url = self.get_image_info()
        new_gapimage, new_nogapimage = self.get_image_complete(gap_image_position, nogap_image_position, gap_image_url,
                                                               nogap_image_url)
        distance = self.get_move_distance(new_gapimage, new_nogapimage)
        self.slid_button(distance)

    def get_image_info(self):
        """
        获得图片的信息，如图片的url，图片的坐标信息。
        共获得两份图片，一份是有缺口的，一份没有缺口。
        :return: gap_image_list和nogap_image_list图片是一系列的div拼接起来的
        """
        gap_image_list = self.wait.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="gt_cut_bg_slice"]')))
                                                                              # '//div[@class="user-login-box"]//div[@class="gt_cut_bg gt_show"]/div[@class="gt_cut_bg_slice"]')))
        nogap_image_list = self.wait.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="gt_cut_fullbg_slice"]')))
        #获取url地址                                                                      # '//div[@class="user-login-box"]//div[@class="gt_cut_fullbg gt_show"]/div[@class="gt_cut_fullbg_slice"]')))
        gap_image_url = re.findall(r'url\("(.*?)"\)', gap_image_list[0].get_attribute('style'))[0]
        nogap_image_url = re.findall(r'url\("(.*?)"\)', nogap_image_list[0].get_attribute('style'))[0]

        #返回所有图片的位置信息 list
        gap_image_position = [re.findall(r'background-position: -(.*?)px -?(.*?)px;', i.get_attribute('style'))[0] for i
                              in gap_image_list]
        nogap_image_position = [re.findall(r'background-position: -(.*?)px -?(.*?)px;', i.get_attribute('style'))[0] for
                                i in nogap_image_list]
        return gap_image_position, nogap_image_position, gap_image_url, nogap_image_url

    def get_image_complete(self, gap_image_position, nogap_image_position, gap_image_url, nogap_image_url):
        """
        将获得混乱的图片，用获得的信息，拼接成正常的图片。
        :param gap_image_position:
        :param nogap_image_position:
        :param gap_image_url:
        :param nogap_image_url:
        :return:
        """
        # BytesIO实现了在内存中读写bytes，我们创建一个BytesIO，然后写入一些bytes
        gap_image_file = BytesIO(requests.get(gap_image_url).content)
        nogap_image_file = BytesIO(requests.get(nogap_image_url).content)
        old_gapimage = Image.open(gap_image_file)#专接图片路径
        new_gapimage = Image.new('RGB', (260, 116))  #拼接图片：58*10 长宽 两行26列 所以新建图片宽26*10 长58*2
        old_nogapimage = Image.open(nogap_image_file)
        new_nogapimage = Image.new('RGB', (260, 116))
        up_count = 0
        down_count = 0
        # 拼接缺口图片  gap_image_position：52个 分为上下两部分 如：-157px -58px（左上顶点） 下部分存在：-157px 0px
        #   其中-58px与0px固定 前面数字上下部分重复并变化
        for i in gap_image_position[:26]:
            #切割图像 粘贴还原下半部分图片
            cut_image = old_gapimage.crop((int(i[0]), 58, int(i[0]) + 10, 116))  # 左上顶点 右下顶点坐标
            new_gapimage.paste(cut_image, (up_count, 0))
            up_count = up_count + 10#图片就是260 粘贴26次
        for i in gap_image_position[26:]:#粘贴还原上半部分图片
            cut_image = old_gapimage.crop((int(i[0]), 0, int(i[0]) + 10, 58))  # 左上顶点，右下顶点
            new_gapimage.paste(cut_image, (down_count, 58))
            down_count = down_count + 10
        # 拼接无缺口图片
        up_count = 0
        down_count = 0
        for i in nogap_image_position[:26]:
            cut_image = old_nogapimage.crop((int(i[0]), 58, int(i[0]) + 10, 116))  # 左上顶点，右下顶点
            new_nogapimage.paste(cut_image, (up_count, 0))
            up_count = up_count + 10
        for i in gap_image_position[26:]:
            cut_image = old_nogapimage.crop((int(i[0]), 0, int(i[0]) + 10, 58))  # 左上顶点，右下顶点
            new_nogapimage.paste(cut_image, (down_count, 58))
            down_count = down_count + 10
        return new_gapimage, new_nogapimage

    def get_move_distance(self, new_gapimage, new_nogapimage):
        def compare_image(p1, p2):
            """
            比较图片的像素
            由于RGB图片一个像素点是三维的，所以循环三次
            算法是两个图层里相同位置的每个像素点RGB值的差
            :return:
            """
            for i in range(3):
                if abs(p1[i] - p2[i]) >= 50:
                    return False
                return True

        for i in range(260): #返回i就是距离
            for j in range(116):
                # 获取图像中某一点的像素的RGB颜色值，参数是一个坐标点。对于图象的不同的模式，getpixel函数返回的值有所不同。
                gap_pixel = new_gapimage.getpixel((i, j))
                nogap_pixel = new_nogapimage.getpixel((i, j))
                if not compare_image(gap_pixel, nogap_pixel):
                    return i

    def slid_button(self, distance):
        """
        根据缺口位置，移动滑块特定的距离distance
        :param diatance:
        :return:
        """
        # 获取滑块元素
        button = self.driver.find_element_by_xpath(
            '//div[@class="gt_slider_knob gt_show"]')
            # '//div[@class="user-login-box"]//div[@class="gt_slider_knob gt_show"]')
        ActionChains(self.driver).click_and_hold(button).perform()
        time.sleep(0.5)
        track_list = self.track(distance - 3)
        # print(track_list)
        for i in track_list:
            ActionChains(self.driver).move_by_offset(i, 0).perform()
        time.sleep(1)
        ActionChains(self.driver).release().perform()

    def track(self, distance):
        """
        规划移动的轨迹
        加速度用到random模块,随机选择给定的加速度  匀速、快速、精准的滑动会判别为机器
        :param distance:
        :return:
        """
        # 匀速移动
        # for i in range(distance):
        #     ActionChains(self.driver).move_by_offset(1, 0).perform()
        # ActionChains(self.driver).move_by_offset(distance-5, 0).perform()
        t = 0.1
        speed = 0
        current = 0
        mid = 3 / 5 * distance
        track_list = []
        while current < distance:
            if current < mid:
                a = random.choice([1, 2, 3])
                # a = 3
            else:
                a = random.choice([-1, -2, -3])
                # a = -4
            move_track = speed * t + 0.5 * a * t ** 2
            track_list.append(round(move_track))
            speed = speed + a * t
            current += move_track
        # 模拟人类来回移动了一小段
        end_track = [1, 0] * 10 + [0] * 10 + [-1, 0] * 10
        track_list.extend(end_track)
        offset = sum(track_list) - distance
        # 由于四舍五入带来的误差,这里需要补回来
        if offset > 0:
            track_list.extend(offset * [-1, 0])
        elif offset < 0:
            track_list.extend(offset * [1, 0])
        return track_list

    def run(self):
        """
        运行函数,在主函数中执行该函数即可
        :return:
        """
        try:
            self.home_page()
        finally:
            time.sleep(0.5)
            self.driver.quit()


if __name__ == '__main__':
    S = SlipCaptcha()
    S.run()