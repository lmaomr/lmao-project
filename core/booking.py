from model.ticket import Ticket

ticket = Ticket()  # 创建车票对象  

def buy_ticket_info():
    """获取用户输入的抢票参数"""
    print("\n=== 请输入抢票参数 ===")

    # 必填项
    ticket.from_station = input("* 出发地: ").strip()
    ticket.to_station = input("* 目的地: ").strip()
    ticket.travel_date = input("* 出行日期(格式:YYYY-MM-DD): ").strip()
    
    return ticket

def buy_ticket_type():
    # 选填项
    ticket.train_types = input("选择车次类型(输入对应数字，可多选，逗号分隔):\n"
                        "1.高铁 2.动车 3.直达 4.特快 5.快速 6.其他 7复兴号 8智能动车组\n"
                        "留空则选择全部: ").strip()
    if ticket.train_types:
        type_map = {
            '1': '高铁', '2': '动车', '3': '直达', 
            '4': '特快', '5': '快速', '6': '其他',
            '7': '复兴号', '8': '智能动车组'
        }
        ticket.train_types = [type_map[num] for num in ticket.train_types.split(',') if num in type_map]
        ticket.train_types = list(set(ticket.train_types))  # 去重
        print(f"选择的车次类型: {ticket.train_types}")

    ticket.allow_transfer = input("是否允许中转(Y/N，默认N): ").strip().upper() == 'Y'

