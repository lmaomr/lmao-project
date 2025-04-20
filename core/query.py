from selenium.webdriver.common.by import By  # 元素定位方式
from selenium.webdriver.support import expected_conditions as EC  # 等待条件
from selenium.webdriver.support.ui import WebDriverWait  # 显式等待
import time  # 时间模块
from config.settings import Settings as settings  # 导入配置模块
from util import helper  # 导入辅助函数模块


def query_tickets(browser, ticket):
        """查询车票并返回车次信息"""
        # 跳转到查询页
        browser.get_web(settings.URLS['query'])
        logger = browser.get_logger("query")  # 设置辅助函数日志记录器
        # 输入查询条件（模拟人工操作）
        WebDriverWait(browser.driver, 10).until(
        EC.element_to_be_clickable((By.ID, "fromStationText"))).click()
        helper.slow_type(browser.driver.find_element(By.ID, "fromStationText"), ticket.from_station + "\n")
        helper.slow_type(browser.driver.find_element(By.ID, "toStationText"), ticket.to_station + "\n")
        helper.slow_type(browser.driver.find_element(By.ID, "train_date"), ticket.travel_date + "\n")
        
        # driver.find_element(By.ID, "_ul_station_train_code").send_keys(ticket.train_types + "\n")

        # 点击查询
        browser.driver.find_element(By.ID,'query_ticket').click()

        # 3. 等待表格加载完成
        WebDriverWait(browser.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "bgc"))
        )

        # # 4. 获取 HTML 表格数据
        # html = driver.page_source
        # soup = BeautifulSoup(html, "html.parser")

        # # 5. 解析表格数据
        # table = soup.find("div", {"t-list"})
        # rows = table.find_all("tr")[1:]  # 跳过表头

        

        # # 清洗所有数据
        # cleaned_data = [clean_row(row) for row in ticket_data]
        # columns = ["车次", "出发时间", "到达时间", "商务座", "一等座", "二等座", "无座"]

        # # 创建DataFrame
        # df = pd.DataFrame(cleaned_data, columns=columns)

        # # 打印完美对齐的表格
        # print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))

        # time.sleep(10)  # 等待表格加载完成

        # 获取结果
        trains = browser.driver.find_elements(By.CSS_SELECTOR, "tr[bed_level_info]")
        if trains: logger.info(f"查询到 {len(trains)} 条车次信息")

        train_infos = []
        for train in trains:
            try:
                info = {
                    # 获取车次信息
                    '车次': train.find_element(By.CSS_SELECTOR, ".number").text,
                    '出发-到达站' : train.find_element(By.CSS_SELECTOR, ".cdz").text.replace("\n", "-"),
                    '出发-到达时间' : train.find_element(By.CSS_SELECTOR, ".cds").text.replace("\n", "-"),
                    '历时' : train.find_element(By.CSS_SELECTOR, ".ls").text.replace("\n", "-"),
                    '商务座' : train.find_element(By.XPATH, "td[2]").text,
                    '优选' : train.find_element(By.XPATH, "td[3]").text,
                    '一等座' : train.find_element(By.XPATH, "td[4]").text,
                    '二等包座' : train.find_element(By.XPATH, "td[5]").text,
                    '高级软座' : train.find_element(By.XPATH, "td[6]").text,
                    '软卧' : train.find_element(By.XPATH, "td[7]").text,
                    '硬卧' : train.find_element(By.XPATH, "td[8]").text,
                    '软座' : train.find_element(By.XPATH, "td[9]").text,
                    '硬座' : train.find_element(By.XPATH, "td[10]").text,
                    '无座' : train.find_element(By.XPATH, "td[11]").text,
                    '其他' : train.find_element(By.XPATH, "td[12]").text
                }
                
                # 过滤车次类型
                # if ticket.train_types and train_infos['车次'][0] not in ticket.train_types:
                #     continue
                    
                train_infos.append(info)
            except Exception:
                continue
        return train_infos

def display_trains(trains):
    """显示车次信息供用户选择"""
    print("\n=== 可预订车次 ===")
    print(f"{'车次':<6}{'出发-到达站':<11}{'出发-到达时间':<10}{'历时':<13}{'商务座':<5}{'优选':<5}{'一等座':<5}"
          f"{'二等座':<5}{'高级软座':<5}{'高级软卧':<5}{'软卧':<5}{'硬卧':<6}{'硬座':<6}{'无座':<6}{'其他':<5}")
    # 打印查询结果
    for info in trains:
        print(
            f""
            f"{info['车次']}\t"
            f"{info['出发-到达站']}\t"
            f"{info['出发-到达时间']}\t"
            f"{info['历时']}\t"
            f"{info['商务座']}\t"
            f"{info['优选']}\t"
            f"{info['一等座']}\t"
            f"{info['二等包座']}\t"
            f"{info['高级软座']}\t"
            f"{info['软卧']}\t"
            f"{info['硬卧']}\t"
            f"{info['软座']}\t"
            f"{info['硬座']}\t"
            f"{info['无座']}\t"
            f"{info['其他']}"
        )
        # for info in trains:
        # print(
        #     f""
        #     f"车次: {info['车次']}\t"
        #     f"出发-到达站: {info['出发-到达站']}\t"
        #     f"出发-到达时间: {info['出发-到达时间']}\t"
        #     f"历时: {info['历时']}\t"
        #     f"商务座: {info['商务座']}\t"
        #     f"优选一等座: {info['优选']}\t"
        #     f"一等座: {info['一等座']}\t"
        #     f"二等包座: {info['二等包座']}\t"
        #     f"高级软座: {info['高级软座']}\t"
        #     f"软卧: {info['软卧']}\t"
        #     f"硬卧: {info['硬卧']}\t"
        #     f"软座: {info['软座']}\t"
        #     f"硬座: {info['硬座']}\t"
        #     f"无座: {info['无座']}\n"
        # )

def select_and_book(driver, trains):
    """让用户选择车次并预订"""
    while True:
        choice = input("\n请选择要预订的车次序号(输入0重新查询，Q退出): ").strip()
        
        if choice.upper() == 'Q':
            return False
        elif choice == '0':
            return True  # 重新查询
            
        try:
            index = int(choice) - 1
            if 0 <= index < len(trains):
                train = trains[index]
                if train['状态'] == '预订':
                    # 点击预订按钮
                    train_elements = driver.find_elements(By.CSS_SELECTOR, "tr[datatran]")
                    train_elements[index].find_element(By.CLASS_NAME, 'btn72').click()
                    time.sleep(2)
                    return book_ticket()
                else:
                    print(f"该车次当前状态为[{train['状态']}]，不可预订")
            else:
                print("序号超出范围，请重新输入")
        except ValueError:
            print("请输入有效的数字序号")

def book_ticket(driver):
    """执行订票流程"""
    try:
        # 选择乘客
        passenger = driver._find_element(['//input[@id="normal_passenger_id"]'], "乘客选择框")
        passenger.click()
        time.sleep(1)
        
        # 提交订单
        submit_btn = driver._find_element(['//a[@id="submitOrder_id"]'], "提交订单按钮")
        submit_btn.click()
        time.sleep(2)
        
        # 确认订单
        confirm_btn = driver._find_element(['//a[@id="qr_submit_id"]'], "确认按钮")
        confirm_btn.click()
        
        print("\n=== 订票成功！请尽快完成支付 ===")
        return True
    except Exception as e:
        print(f"订票失败: {str(e)}")
        driver.save_screenshot('book_error.png')
        return False
