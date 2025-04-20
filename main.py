from core.login import Login
from core import booking
from util import logger
from core import query
from model.ticket import Ticket

if __name__ == "__main__":
    main_logger = logger.setup_logger("main")  # 设置主日志记录器
    login_instance = None
    
    try:
        # 创建登录实例
        login_instance = Login()
        
        if login_instance.login():
            main_logger.info("开始执行购票流程...")
            ticket = Ticket()  # 创建车票对象
            ticket = booking.buy_ticket_info  # 获取用户输入的抢票参数
            tickets = query.query_tickets(login_instance.browser, ticket)  # 查询车票
            if tickets:
                 query.display_trains(tickets)
            else:
                main_logger.info("没有符合条件的车票。")
    except Exception as e:
        main_logger.error(f"程序异常: {str(e)}")
    finally:
            # 显式关闭浏览器是良好实践，确保资源释放和避免僵尸进程
            if login_instance and hasattr(login_instance, 'driver') and login_instance.driver:
                login_instance.driver.quit()
