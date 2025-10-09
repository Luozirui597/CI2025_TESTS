#这个文件是测试文件，用来测试很多莫名其妙出现或者想到看到的问题和想法



#突然想到的本科时的问题，现在再做一次
#找零计算器，面额100,50,20,10,5,1,0.5
#要求找零金额四舍五入到0.5
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

DENOMS = [Decimal('100'), Decimal('50'), Decimal('20'),
          Decimal('10'), Decimal('5'), Decimal('1'), Decimal('0.5')]

def parse_money(prompt: str) -> Decimal:
    while True:
        s = input(prompt).strip()
        try:
            # 使用 Decimal 更稳，允许诸如 238.5 / 238,50（逗号替换为点）
            s = s.replace(',', '.')
            v = Decimal(s)
            if v < 0:
                print("金额不能为负，请重新输入。")
                continue
            return v
        except (InvalidOperation, AttributeError):
            print("输入格式不正确，请输入数字。如：238.5 或 500")

def normalize_to_half(x: Decimal) -> Decimal:
    """将金额四舍五入到 0.5 的步进：乘 2 取整 / 再除 2"""
    units = (x * 2).quantize(Decimal('1'), rounding=ROUND_HALF_UP)  # 个数（每个代表0.5）
    return (units / 2).quantize(Decimal('0.0'))  # 保留1位小数

def make_change(price: Decimal, paid: Decimal):
    if paid < price:
        raise ValueError("付款金额小于商品金额。")

    raw_change = paid - price
    change = normalize_to_half(raw_change)  # 规范到 0.5 步进
    units = int((change * 2))               # 用 0.5 为单位进行贪心（整数）
    result = {d: 0 for d in DENOMS}

    # 将每个面额映射为 0.5 单位数：100→200, 50→100, …, 1→2, 0.5→1
    denom_units = [int(d * 2) for d in DENOMS]

    remain = units
    for d, u in zip(DENOMS, denom_units):
        cnt, remain = divmod(remain, u)
        result[d] = cnt

    assert remain == 0
    return change, result, raw_change

def main():
    print("=== 找零计算器（面额：100, 50, 20, 10, 5, 1, 0.5）===")
    price = parse_money("商品金额：")
    paid  = parse_money("客户付款：")

    try:
        change, breakdown, raw_change = make_change(price, paid)
    except ValueError as e:
        print("错误：", e)
        return

    # 提示是否发生了 0.5 步进的四舍五入
    if normalize_to_half(raw_change) != raw_change:
        print(f"注意：应找零 {raw_change} 已按 0.5 的最小单位四舍五入为 {change}")

    print(f"\n应找零：{change}")
    print("零钱组成：")
    for d in DENOMS:
        # 显示时去掉无意义的小数 .0
        face = int(d) if d == d.to_integral_value() else d
        print(f"  {face:>4}: {breakdown[d]}")

if __name__ == "__main__":
    main()
